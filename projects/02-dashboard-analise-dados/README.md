# 02 — Dashboard de insights de mercado

## O que é

Uma interface leve para transformar textos qualitativos em um resumo operacional: principais pontos, sinais positivos, riscos e perguntas para a próxima decisão.

A versão entregue funciona offline com um extrator demonstrativo baseado em regras. Isso permite apresentar o fluxo sem expor credenciais. A integração com LLM é opcional e deve ser ativada apenas com dados autorizados.

## Como executar

```bash
pip install -r requirements.txt
streamlit run app.py
```

## Entrada esperada

Um arquivo `.txt` ou `.csv` com uma coluna `text`, ou texto colado diretamente na interface.

## Saída

- Resumo executivo;
- Temas identificados;
- Sinais e riscos;
- Perguntas recomendadas;
- Exportação em JSON.

## Métricas a instrumentar

- Tempo para produzir um briefing;
- Número de documentos analisados;
- Concordância entre resumo e avaliação humana;
- Taxa de edição após geração;
- Custo e latência por documento.

## Privacidade e segurança

- Não subir dados pessoais ou informações confidenciais no demo.
- Em produção, aplicar anonimização, controle de acesso e retenção mínima.
- Exibir a origem dos trechos usados em cada insight.
- Manter revisão humana para decisões de alto impacto.
