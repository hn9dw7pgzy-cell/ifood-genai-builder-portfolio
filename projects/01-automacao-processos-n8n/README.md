# 01 — Automação inteligente de triagem

## Visão executiva

Este blueprint representa um processo de entrada de solicitações que hoje depende de leitura e encaminhamento manual. A proposta é usar automação para estruturar a entrada, utilizar um LLM apenas onde há ambiguidade semântica e registrar a decisão para auditoria.

## Fluxo

1. Receber a solicitação por webhook.
2. Validar campos mínimos e gerar um identificador.
3. Classificar intenção, urgência e categoria.
4. Extrair entidades úteis para o atendimento.
5. Aplicar regras de segurança e confiança.
6. Encaminhar para o sistema ou fila adequada.
7. Registrar entrada, decisão, latência e fallback.

O diagrama está em [`workflow_diagram.mmd`](workflow_diagram.mmd) e a imagem renderizada em [`workflow_diagram.png`](workflow_diagram.png).

## Contrato de saída sugerido

```json
{
  "category": "delivery_issue",
  "priority": "medium",
  "summary": "Resumo curto da solicitação",
  "entities": {
    "order_id": "optional",
    "city": "optional"
  },
  "confidence": 0.87,
  "needs_human_review": false
}
```

## Critérios de qualidade

- Classificação correta avaliada em um conjunto rotulado.
- Fallback automático quando a confiança fica abaixo do limiar.
- Nenhum dado sensível enviado ao modelo sem necessidade.
- Logs suficientes para reconstruir uma decisão.
- Tempo e custo por execução acompanhados separadamente.

## Implementação no n8n

O arquivo [`workflow.example.json`](workflow.example.json) é um esqueleto importável/documental. Antes de usar em produção, configure credenciais, endpoints, políticas de retenção e nós de observabilidade.

## Resultado prático demonstrativo

Para testar sem usar dados reais ou consumir uma API, execute:

```bash
python demo_local.py
```

O exemplo usa [`sample-request.json`](sample-request.json) como entrada e [`sample-llm-response.json`](sample-llm-response.json) como resposta simulada da LLM. O resultado esperado é uma classificação `order_issue`, confiança `0.96` e roteamento automático para a fila correspondente. Em uma execução real, o conteúdo de `sample-llm-response.json` seria produzido pelo nó **HTTP Request**.

## Configuração do `.env`

O arquivo [`n8n.env.example`](n8n.env.example) serve como modelo. Faça uma cópia local e preencha os valores sem comitar o arquivo:

```bash
cp n8n.env.example .env
```

Variáveis principais:

```dotenv
LLM_ENDPOINT=https://api.openai.com/v1/chat/completions
LLM_MODEL=gpt-4o-mini
OPENAI_API_KEY=cole_sua_chave_somente_no_ambiente_local
```

Se estiver usando outro provedor compatível, substitua `LLM_ENDPOINT`, `LLM_MODEL` e a chave correspondente. O endpoint precisa aceitar uma requisição `POST` com `messages` e retornar uma resposta de chat ou JSON estruturado.

### Opção A — ambiente local com Docker

Na pasta do projeto n8n, carregue o `.env` no processo do n8n:

```bash
docker run --rm -it \
  --name n8n-ai-builder \
  --env-file .env \
  -p 5678:5678 \
  docker.n8n.io/n8nio/n8n
```

Abra `http://localhost:5678`, importe `workflow.example.json` e configure o webhook. Para um ambiente persistente, use volume Docker e defina também uma `N8N_ENCRYPTION_KEY` longa e aleatória.

> O `.env` não deve ser enviado ao GitHub, incluído em screenshots ou colado em mensagens. O `.gitignore` do repositório já ignora arquivos `.env`.

### Opção B — credencial do n8n (recomendada)

Para um fluxo compartilhado ou produção, prefira uma credencial no n8n em vez de acessar a chave por expressão:

1. Abra **Credentials → New credential → Header Auth**.
2. Dê um nome como `LLM Provider — API Key`.
3. Configure o cabeçalho `Authorization` com o valor `Bearer SUA_CHAVE`.
4. No nó **HTTP Request**, escolha essa credencial e não escreva a chave no JSON do workflow.
5. Adicione o cabeçalho `Content-Type: application/json`.

Essa abordagem permite trocar ou revogar a chave sem alterar o workflow exportado. Ao exportar o fluxo, confirme que a opção de incluir dados de credenciais está desativada.

## Configuração do nó HTTP Request

Para um endpoint de chat compatível com OpenAI, use:

**Method:** `POST`
**URL:** `={{$env.LLM_ENDPOINT}}`
**Authentication:** credencial `Header Auth` (recomendado)
**Send Body:** ativado
**Body Content Type:** JSON

Exemplo de corpo com saída estruturada:

```json
{
  "model": "={{$env.LLM_MODEL}}",
  "temperature": 0.1,
  "messages": [
    {
      "role": "system",
      "content": "Classifique a solicitação e retorne somente JSON válido com category, priority, summary, entities, confidence e needs_human_review. Não invente dados."
    },
    {
      "role": "user",
      "content": "={{$json.text}}"
    }
  ],
  "response_format": {"type": "json_object"}
}
```

Depois do HTTP Request, use um nó **Code** ou **Edit Fields** para extrair o conteúdo retornado. Em muitos endpoints compatíveis com OpenAI, o texto fica em `$json.choices[0].message.content`. Converta esse texto para JSON somente depois de validar se a resposta existe e é parseável. Se houver erro, timeout ou confiança abaixo do limiar, encaminhe para revisão humana.

## Teste seguro de ponta a ponta

1. Use uma solicitação sintética, sem dados pessoais.
2. Execute o webhook manualmente pelo editor do n8n.
3. Confirme o payload recebido no nó **Normalizar**.
4. Verifique a requisição e a resposta do nó **Classificar com LLM**.
5. Teste uma resposta inválida e uma confiança baixa para validar o fallback.
6. Só depois conecte CRM, planilha ou fila real.

## Cuidados de custo, privacidade e confiabilidade

- Defina limite de tamanho do texto antes de enviá-lo ao modelo.
- Remova dados pessoais e identificadores desnecessários.
- Configure timeout, tentativas limitadas e backoff.
- Registre latência, tokens/custo quando disponível e motivo do fallback.
- Não use a saída do LLM como decisão final em casos sensíveis sem revisão humana.
- Faça versionamento do prompt e avalie o fluxo com um conjunto rotulado antes de declarar impacto.

## Métricas antes de afirmar impacto

| Métrica | Linha de base | Meta inicial | Resultado real |
|---|---:|---:|---:|
| Tempo médio de triagem | a medir | reduzir | a medir |
| Taxa de roteamento correto | a medir | aumentar | a medir |
| Fallback para humano | a medir | controlar | a medir |
| Custo por solicitação | a medir | acompanhar | a medir |

> Não utilizar “65% de redução” sem evidência de medição comparável.
