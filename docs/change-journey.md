# Jornada completa de uma mudança

Cenário de uma mudança R2 de aplicação, da demanda ao feedback de produção. As ferramentas citadas são substituíveis por adaptadores.

~~~mermaid
flowchart TB
  I["1. Intake"] --> R["2. Refinamento"]
  R --> D["3. Design"]
  D --> B["4. Build e PR"]
  B --> V["5. Test e Security"]
  V --> A["6. Review e aprovação"]
  A --> L["7. Release e canary"]
  L --> O["8. Observação"]
  V -->|falha| B
  A -->|rejeição| R
  L -->|guardrail violado| X["Rollback e incidente"]
~~~

## Passos e sistemas de registro

| Etapa | Ação | Agente | Evidência/gate | Sistema de registro |
|---|---|---|---|---|
| Intake | webhook cria change_id e snapshot | Control plane | source, owner, correlação | work management + orquestrador |
| Refinamento | critérios, dados, dependências e risco | Product | Definition gate | work item + evidence |
| Design | ADR, contratos, threat model e rollback | Architecture | Design gate | SCM + evidence |
| Build | sandbox, implementação e PR | Developer | diff, commit e SBOM | SCM + CI |
| Verificação | Test e Security em paralelo no mesmo commit | Test e Security | testes, scans e findings | CI/checks + evidence |
| Decisão | review e aprovação vinculada ao digest | Reviewer + humano | Approval gate | PR + audit log |
| Release | pipeline promove o mesmo digest e inicia canary | Release | Release gate | registry + CD |
| Observação | SLOs, custo e outcome fecham workflow | Release/Incident | Observation gate | telemetry + orquestrador |

~~~mermaid
sequenceDiagram
  actor H as Humano
  participant W as Work management
  participant O as Control plane
  participant A as Agents
  participant G as SCM, CI e CD
  participant T as Telemetry
  H->>W: cria demanda
  W->>O: webhook assinado
  O->>A: Product e Architecture
  A->>G: critérios, ADR e contratos
  O->>A: Developer em sandbox
  A->>G: branch, commit e PR
  G->>O: build e artifact digest
  par verificação
    O->>A: Test
  and segurança
    O->>A: Security
  end
  A->>G: checks e evidências
  O->>H: risco, diff e digest
  H->>O: aprovação autenticada
  O->>G: promover digest
  G->>T: deploy marker e canary
  T->>O: SLOs e guardrails
  O->>W: status final e links
~~~

Mudança no diff recalcula risco; alteração do digest invalida aprovação; falha de teste ou segurança retorna ao Developer; rejeição retorna a Refinement ou Design; guardrail violado aciona rollback pelo pipeline e Incident Review.

O usuário trabalha em Jira, Azure Boards, GitHub, PR checks e IDE. O Developer Portal consolida workflow, risco, custo, evidências e aprovações. ChatOps serve para consulta e notificação, não como interface exclusiva de decisões críticas.
