# Modelo de runtime dos agentes

## Decisão operacional

Os oito papéis são **definições lógicas versionadas executadas por um runtime compartilhado**. Eles não exigem oito serviços persistentes. Cada etapa cria um worker efêmero com identidade, contexto, ferramentas e budget específicos.

Os repositórios sdlc-role-agent podem continuar como pacotes de definição, testes e avaliações. Autenticação, telemetria, policy, MCP, retry e checkpoint pertencem ao runtime/SDK compartilhado.

## Separação de responsabilidades

| Elemento | Contém | Não contém |
|---|---|---|
| Agent Definition | finalidade, prompt digest, modelos, I/O schemas, tools, budget e evals | estado do workflow e credenciais |
| Workflow Definition | estados, paralelismo, gates, retries e compensações | prompts e chamadas diretas a fornecedores |
| Tool Definition | capability, schemas, risco, idempotência e endpoint MCP | autoridade implícita |
| Runtime | contexto, model call, tool loop e telemetria | decisão de negócio do workflow |
| Orquestrador | estado canônico, agenda, timeout, aprovação e retomada | execução de código gerado |

## Ciclo de uma execução

~~~mermaid
sequenceDiagram
  participant O as Orquestrador
  participant R as Runtime
  participant P as Policy
  participant M as Modelo
  participant G as MCP Gateway
  participant E as Evidence Store
  O->>R: iniciar etapa e capability grant
  R->>P: validar identidade, risco e budget
  P-->>R: allow, deny ou approval
  R->>M: contexto mínimo e instruções
  M-->>R: saída estruturada ou tool request
  R->>G: chamada com identidade e change_id
  G->>P: autorizar efeito
  P-->>G: decisão
  G-->>R: resultado sanitizado
  R->>E: evidências, hashes e telemetria
  R-->>O: outcome e checkpoint
~~~

## Estado, composição e limites

O orquestrador é dono do estado durável; o worker mantém somente scratch state. Resultados grandes ficam no Evidence Store. Retomadas criam novo agent_run_id e side effects usam idempotency key.

Test e Security podem executar em paralelo. Falhas determinísticas retornam ao Developer. Architecture pode participar por subworkflow. Agentes não chamam outros agentes livremente: toda composição passa pelo orquestrador e pelo audit log.

Cada execução limita passos, tokens, custo, duração, tool calls, retries, CPU, memória e egress. Ao atingir o limite, produz checkpoint e termina; nunca amplia o próprio budget.

## Implementação de referência

O modelo descrito nesta página está implementado em [agentic-sdlc-runtime](https://github.com/leandrosflora/agentic-sdlc-runtime). O runtime carrega definições declarativas dos oito papéis, monta contexto governado, chama um Model Gateway, limita tools pelo MCP Gateway, emite eventos e evidências e mantém checkpoints retomáveis.

~~~mermaid
flowchart LR
  D["Agent Definition"] --> R["Shared Runtime"]
  C["Context Builder"] --> R
  R --> M["Fake ou Real Model Gateway"]
  R --> T["MCP Gateway"]
  R --> E["Events e Evidence"]
  R --> P["Checkpoint"]
  P -->|resume| R
~~~

A implementação local usa filesystem para demonstrar os contratos. Em produção, Evidence Store, Event Store e Checkpoint Store devem ser substituídos por backends duráveis sem alterar as definições dos agentes.
