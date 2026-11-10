# Portfólio GenAI — AI Builder (Negócios)

> Portfólio demonstrativo de aplicações de IA para eficiência operacional, automação e apoio à decisão.

Este repositório apresenta como transformo problemas de negócio em protótipos funcionais usando LLMs, APIs, automação low-code e interfaces leves. O foco é conectar tecnologia a uma hipótese mensurável de valor — tempo economizado, qualidade da triagem, velocidade de resposta e clareza para decisão.

## Projetos

### 01. Automação inteligente de triagem

Fluxo de referência para receber uma solicitação, normalizar o conteúdo, classificar a intenção com IA, extrair campos estruturados e encaminhar a demanda para o próximo sistema.

- **Problema:** triagem manual de solicitações não estruturadas.
- **Solução:** webhook + classificação semântica + roteamento + registro de auditoria.
- **Stack:** n8n, webhook, LLM, Google Sheets/CRM e APIs REST.
- **Métrica a acompanhar:** tempo de ciclo, taxa de roteamento correto e volume processado sem intervenção.
- [Ver documentação](projects/01-automacao-processos-n8n/README.md)

### 02. Mini-ferramenta de insights de mercado

Aplicação Streamlit para carregar textos, sumarizar informações e transformar conteúdo qualitativo em sinais acionáveis para uma equipe de negócio.

- **Problema:** leitura manual e dispersa de grandes volumes de texto.
- **Solução:** interface simples com sumarização local demonstrativa e integração opcional com LLM.
- **Stack:** Python, Streamlit, pandas e API compatível com OpenAI.
- **Métrica a acompanhar:** tempo médio por análise, cobertura dos documentos e avaliação humana da utilidade.
- [Ver documentação](projects/02-dashboard-analise-dados/README.md)

## Como executar o dashboard

```bash
cd projects/02-dashboard-analise-dados
python -m venv .venv
source .venv/bin/activate  # Windows: .venv\\Scripts\\activate
pip install -r requirements.txt
streamlit run app.py
```

A aplicação funciona em **modo demonstrativo sem API key**. Para testar uma integração real, copie `.env.example` para `.env` e informe uma chave em `OPENAI_API_KEY` e, se necessário, `OPENAI_API_BASE`.

## Princípios de construção

1. Começar pelo problema e pelo fluxo atual, não pela ferramenta.
2. Prototipar com o menor número de componentes possível.
3. Tornar entradas, saídas, critérios e falhas observáveis.
4. Medir impacto com uma linha de base antes de afirmar resultado.
5. Tratar números de impacto como **a validar** até que exista medição real.

## Sobre as métricas

Os projetos deste repositório são demonstrações e benchmarks de processo. Não há resultados de cliente ou de operação produtiva declarados aqui. Percentuais, horas economizadas e ROI devem ser preenchidos somente após medição documentada.

## Próximas evoluções

- Conectar o fluxo a uma base de chamados real ou conjunto anonimizado.
- Adicionar avaliação offline de classificação e extração.
- Registrar latência, custo por execução e taxa de fallback.
- Publicar uma versão hospedada do dashboard com dados sanitizados.

## Personalização

Substitua os campos entre colchetes no currículo e nos textos do portfólio:

- `[Seu nome]`
- `[Curso e universidade]`
- `[LinkedIn]`
- `[GitHub]`
- `[E-mail]`

Este repositório é um ponto de partida técnico e editorial para uma candidatura à trilha **AI Builder (Negócios)**.
