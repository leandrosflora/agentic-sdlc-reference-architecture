# ADR 0001 — Núcleo agnóstico com adaptadores de SDLC

- **Status:** Aceito
- **Data:** 2026-07-21

## Contexto

A plataforma deve operar com GitHub, GitLab, Azure DevOps, Jira, Jenkins, Argo CD, segurança e observabilidade sem transferir o estado canônico do workflow ou a autoridade dos agentes para um fornecedor. Acoplar agentes diretamente a cada produto duplicaria prompts, políticas, identidade, auditoria e orquestração.

## Decisão

Adotar **núcleo agnóstico e integrações específicas nas bordas**. O control plane mantém estado, políticas, identidade, budgets, evidências e coordenação. Ferramentas do SDLC são canais de experiência, sistemas de registro ou executores. Adaptadores traduzem seus modelos para contratos canônicos: WorkItem, Requirement, Approval, Repository, ChangeSet, PullRequest, Evidence, Build, Artifact, Deployment, Telemetry e Incident.

Todo adaptador deve:

1. autenticar webhooks e preservar identidade e correlação;
2. traduzir eventos sem perder o payload original referenciado;
3. declarar capabilities, schemas, classe de risco e idempotência;
4. acessar ferramentas pelo MCP Gateway ou integração controlada;
5. não manter estado canônico do workflow;
6. falhar fechado para escrita sem policy, identidade ou auditoria.

~~~mermaid
flowchart LR
  T["Ferramentas SDLC"] --> A["Adaptadores"]
  A --> C["Contratos canônicos"]
  C --> P["Control Plane"]
  P --> G["MCP Gateway"]
  G --> A
~~~

## Sistemas de registro

| Informação | Sistema canônico |
|---|---|
| Estado e transições do workflow | Orquestrador durável |
| Requisito e ownership | Jira, Azure Boards ou GitHub Issues |
| Código, commits e pull requests | SCM configurado |
| Artefato promovível | Registry corporativo |
| Evidências e auditoria | Evidence Store e Audit Log |
| Políticas e definições de agentes | Repositórios versionados |
| Telemetria operacional | Plataforma de observabilidade |

## Consequências

Benefícios: troca de fornecedor sem reescrever agentes, governança consistente, integração profunda por adaptador e reutilização entre toolchains.

Custos: contratos canônicos precisam de versionamento; adaptadores exigem ownership, SLO e testes de conformidade; particularidades de fornecedor usam extensões namespaced sem contaminar o núcleo.

## Alternativas rejeitadas

- **Agentes embutidos em cada ferramenta:** fragmentam governança e autoridade.
- **GitHub Actions como control plane:** pipeline não substitui workflow durável, approvals e memória.
- **Integração genérica única:** perde semântica relevante de cada fornecedor.
