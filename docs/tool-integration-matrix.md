# Matriz agente × ferramenta × operação

A matriz apresenta capacidades máximas. A autorização efetiva depende de projeto, risco, ambiente, evidências e policy.

| Agente | Work management | SCM / PR | CI e qualidade | CD / artefatos | Observabilidade / ITSM |
|---|---|---|---|---|---|
| Product | ler demanda; escrever critérios | ler contexto | ler evidências | — | ler feedback |
| Architecture | ler requisito; registrar decisão | escrever ADR e contratos em branch | validar regras | ler manifests | ler dependências e impacto |
| Developer | ler escopo aprovado | criar branch, commit e PR | disparar build/teste não produtivo | candidato somente via CI | logs não produtivos |
| Test | ler critérios | escrever testes em branch autorizada | executar suites e publicar evidência | ler candidato | ler resultados |
| Security | registrar achados | comentar ou bloquear PR | consumir scans | atestar ou bloquear digest | abrir finding/incidente |
| Reviewer | ler requisito e decisões | emitir review independente | ler evidências | ler digest | ler impacto |
| Release | ler change e aprovação | ler commit e tag | validar gates | promover digest e rollback aprovado | validar health checks |
| Incident | criar/enriquecer incidente | correlacionar commits e propor hotfix | ler pipelines | propor rollback | consultar telemetria |

## Classes de operação

| Classe | Exemplos | Controle mínimo |
|---|---|---|
| Read-only | issue, diff, logs e status | escopo de projeto e auditoria |
| Write non-production | comentário, branch, PR e build | capability, policy e idempotência |
| Delivery | publicar candidato e promover digest | gates, provenance e aprovação |
| Privileged | IAM, segredo e ação destrutiva | proposta do agente e execução humana |

## Mapeamento por fornecedor

| Domínio | GitHub | Azure DevOps | Alternativas |
|---|---|---|---|
| WorkItem | Issues | Azure Boards | Jira |
| Repository/PullRequest | Repositories/PRs | Azure Repos/PRs | GitLab, Bitbucket |
| Build/Evidence | Actions/Checks | Azure Pipelines | Jenkins, Tekton |
| Deployment | Environments/Actions | Releases/Pipelines | Argo CD, Spinnaker |
| Artifact | Packages/registry | Artifacts/registry | ECR, Nexus, Artifactory |
| Incident/Telemetry | Checks e links | Boards e links | ServiceNow, Dynatrace, Datadog |

Recursos exclusivos usam extensões namespaced. Nenhum adaptador altera estado de workflow sem evento validado pelo control plane.
