import json
import os
import re
from collections import Counter

import streamlit as st

st.set_page_config(page_title="Insight Desk", page_icon="ID", layout="wide")

STOPWORDS = {"para", "com", "uma", "que", "dos", "das", "por", "não", "mais", "como", "uma", "sobre", "quando", "este", "esta", "isso", "eles", "elas", "entre", "sem", "nos", "nas", "aos", "ainda", "muito", "pelo", "pela", "seu", "sua"}


def demo_analyze(text: str) -> dict:
    sentences = [s.strip() for s in re.split(r"[.!?\\n]+", text) if s.strip()]
    words = re.findall(r"[A-Za-zÀ-ÿ]{4,}", text.lower())
    terms = [w for w in words if w not in STOPWORDS]
    top_terms = [term for term, _ in Counter(terms).most_common(6)]
    positives = [s for s in sentences if re.search(r"crescimento|melhora|positivo|eficiente|rápido|aumento|ganho", s, re.I)]
    risks = [s for s in sentences if re.search(r"risco|problema|atraso|queda|custo|difícil|reclama", s, re.I)]
    summary = " ".join(sentences[:3]) if sentences else "Inclua um texto para gerar um resumo demonstrativo."
    return {
        "summary": summary[:500],
        "themes": top_terms,
        "signals": positives[:4],
        "risks": risks[:4],
        "questions": [
            "Qual decisão de negócio este insight deve orientar?",
            "Que evidência adicional reduziria a incerteza?",
            "Como medir a mudança após a ação?",
        ],
        "mode": "demo-local",
    }


def llm_analyze(text: str) -> dict | None:
    # Integração opcional e deliberadamente simples: o demo não depende dela.
    try:
        from openai import OpenAI
        client = OpenAI(api_key=os.environ["OPENAI_API_KEY"], base_url=os.getenv("OPENAI_API_BASE"))
        response = client.chat.completions.create(
            model=os.getenv("OPENAI_MODEL", "gpt-4o-mini"),
            temperature=0.2,
            response_format={"type": "json_object"},
            messages=[
                {"role": "system", "content": "Retorne JSON com summary, themes, signals, risks e questions. Seja conciso e não invente fatos."},
                {"role": "user", "content": text},
            ],
        )
        data = json.loads(response.choices[0].message.content)
        data["mode"] = "llm"
        return data
    except Exception:
        return None


st.title("Insight Desk")
st.caption("Protótipo de apoio à decisão — dados demonstrativos, sem resultados de produção")

with st.sidebar:
    st.subheader("Configuração")
    use_llm = st.toggle("Usar LLM configurado", value=False)
    st.info("Sem API key, o protótipo usa análise local por regras para manter o fluxo reproduzível.")

sample = """Clientes relatam melhora na velocidade de entrega em regiões centrais.\nA operação ainda enfrenta atraso em horários de pico e aumento de custo logístico.\nA equipe identificou uma oportunidade de testar uma nova janela de despacho."""
text = st.text_area("Cole um conjunto de relatos, notas ou comentários", value=sample, height=180)

if st.button("Gerar briefing", type="primary"):
    result = llm_analyze(text) if use_llm else None
    result = result or demo_analyze(text)
    st.session_state["result"] = result

result = st.session_state.get("result")
if result:
    st.divider()
    st.subheader("Resumo executivo")
    st.write(result.get("summary", "Sem resumo."))

    col1, col2, col3 = st.columns(3)
    with col1:
        st.metric("Modo", result.get("mode", "demo-local"))
    with col2:
        st.metric("Temas", len(result.get("themes", [])))
    with col3:
        st.metric("Sinais + riscos", len(result.get("signals", [])) + len(result.get("risks", [])))

    left, right = st.columns(2)
    with left:
        st.subheader("Temas recorrentes")
        for item in result.get("themes", []):
            st.write(f"• {item}")
        st.subheader("Sinais positivos")
        for item in result.get("signals", []):
            st.success(item)
    with right:
        st.subheader("Riscos ou fricções")
        for item in result.get("risks", []):
            st.warning(item)
        st.subheader("Perguntas para a decisão")
        for item in result.get("questions", []):
            st.write(f"• {item}")

    st.download_button(
        "Baixar briefing em JSON",
        data=json.dumps(result, ensure_ascii=False, indent=2),
        file_name="briefing.json",
        mime="application/json",
    )
else:
    st.markdown("### Como demonstrar o projeto")
    st.write("Cole relatos, gere o briefing e mostre como a interface transforma texto disperso em uma pauta objetiva para decisão.")
