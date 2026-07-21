# Product Agent funcional

O [sdlc-product-agent](https://github.com/leandrosflora/sdlc-product-agent) implementa a primeira vertical funcional da arquitetura.

~~~mermaid
sequenceDiagram
  actor U as Usuário
  participant I as GitHub Issue
  participant P as Product Agent
  participant O as OPA
  participant R as Shared Runtime
  participant E as Evidence Store

  U->>I: abre ou edita Issue
  I->>P: issues event
  P->>O: requirements.update
  O-->>P: allow ou deny
  P->>R: contexto e objetivo
  R-->>P: critérios estruturados
  P->>I: comentário idempotente
  P->>E: context, output, event e checkpoint
~~~

## Entrada

- número, título, corpo e URL do Issue;
- repositório como project_id;
- texto do Issue tratado como contexto não confiável;
- change_id determinístico derivado do número do Issue.

## Saída obrigatória

~~~json
{
  "acceptance_criteria": [
    "critério específico e verificável"
  ],
  "assumptions": [],
  "risk": "R1"
}
~~~

O agente rejeita saída sem critérios, strings vazias e risco fora de R0/R1.

## Operação no GitHub

O workflow responde a Issue aberto, editado ou rotulado e também aceita execução manual com issue_number. O comentário contém um marker estável, por isso novas execuções atualizam a resposta anterior.

O artifact do workflow preserva por 90 dias:

- summary estruturado;
- context evidence;
- output evidence;
- agent event;
- checkpoint.

## Modelos

Sem secrets, usa Fake Model Gateway determinístico. Com MODEL_BASE_URL, MODEL_API_KEY e MODEL_NAME, utiliza o gateway OpenAI-compatible do runtime.

## Controles

- autorização OPA antes da execução;
- conteúdo externo delimitado e com proveniência;
- credentials fora do contexto;
- grants de tools por definição;
- evidências correlacionadas por change_id e agent_run_id.
