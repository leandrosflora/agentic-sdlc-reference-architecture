# Agentic SDLC Reference Architecture

Arquitetura de referência para uma plataforma de engenharia de software orientada por agentes, cobrindo o fluxo completo entre demanda e produção. O objetivo não é criar “um agente que escreve código”, mas um **sistema sociotécnico governado**, no qual agentes especializados trabalham com contexto, ferramentas e permissões mínimas, enquanto decisões de risco permanecem sob aprovação humana.

> Esta proposta deriva os princípios de plataforma, governança, segurança, observabilidade e FinOps da [Enterprise AI Platform Reference Architecture](https://github.com/leandrosflora/enterprise-ai-platform-reference-architecture), adotada como fonte conceitual da verdade, e os aplica ao domínio de SDLC.

## Objetivos

- Orquestrar agentes especializados do requisito ao feedback de produção.
- Preservar segregação de funções: quem implementa não aprova nem publica.
- Manter rastreabilidade verificável entre requisito, decisão, código, teste, evidência, aprovação, artefato e deploy.
- Aplicar segurança por padrão com identidade de workload, isolamento, permissões por agente e policy-as-code.
- Medir qualidade, velocidade, autonomia, confiabilidade e custo por mudança.
- Permitir intervenção humana, cancelamento, rollback e limitação de blast radius em todas as fases críticas.

## Fluxo principal

```mermaid
flowchart LR
    E[Epic / Requisito] --> P[Product Agent]
    P --> A[Architecture Agent]
    A --> D[Development Agent]
    D --> T[Test Agent]
    T --> S[Security Agent]
    S --> R{Review / Approval}
    R -->|aprovado| C[CI/CD]
    R -->|rejeitado| P
    C --> O[Produção + Observabilidade]
    O --> I[Incident Agent]
    O -->|feedback| P
    I -->|evidência e aprendizado| P
```

Cada transição produz um **evidence bundle** assinado; o orquestrador somente avança quando contratos, políticas e gates da etapa forem satisfeitos.

## Agentes e segregação de funções

| Agente | Responsabilidade | Pode escrever em | Não pode |
|---|---|---|---|
| Product | Refinar requisitos e critérios de aceite | backlog e `requirements/` | alterar código ou aprovar release |
| Architecture | Produzir C4, ADRs, contratos e análise de blast radius | `architecture/` e `contracts/` | publicar artefatos |
| Developer | Implementar mudanças dentro do escopo aprovado | branch/ambiente efêmero | aprovar o próprio PR ou acessar produção |
| Test | Criar e executar testes; avaliar cobertura e mutações | testes e evidências | reduzir gates ou publicar |
| Security | SAST, SCA, secrets e threat modeling | achados e evidências | editar a implementação silenciosamente |
| Reviewer | Verificar qualidade, escopo, arquitetura e evidências | parecer de revisão | implementar ou fazer deploy |
| Release | Preparar versão, rollout e rollback | manifesto de release | ignorar aprovação humana/política |
| Incident | Correlacionar logs, traces, deploys e mudanças | timeline e proposta de remediação | executar ação destrutiva sem aprovação |

A matriz detalhada de permissões e gates está em [`docs/governance.md`](docs/governance.md).

## Arquitetura

```mermaid
flowchart TB
  subgraph EXP[Experience & Integration]
    GH[GitHub / Issues / PRs]
    PORTAL[Developer Portal]
    CICD[CI/CD]
    CHAT[ChatOps]
  end

  subgraph CP[Agent Control Plane]
    API[Workflow API]
    ORCH[Durable Orchestrator]
    REG[Agent & Tool Registry]
    POLICY[Policy Decision Point]
    EVAL[Evaluation Service]
    COST[Token & Cost Controller]
  end

  subgraph AP[Agent Plane]
    PROD[Product]
    ARCH[Architecture]
    DEV[Developer]
    TEST[Test]
    SEC[Security]
    REV[Reviewer]
    REL[Release]
    INC[Incident]
  end

  subgraph KP[Knowledge & Data Plane]
    MEM[(Project Memory)]
    ART[(Evidence / Artifacts)]
    AUDIT[(Immutable Audit Log)]
    META[(Traceability Graph)]
  end

  subgraph EP[Execution Plane]
    MCP[MCP Gateway]
    SBX[Ephemeral Sandboxes]
    TOOLS[Git / CI / Cloud / Observability]
  end

  EXP --> API --> ORCH
  ORCH --> AP
  ORCH --> POLICY
  ORCH --> EVAL
  ORCH --> COST
  AP --> MCP --> TOOLS
  MCP --> POLICY
  DEV --> SBX
  TEST --> SBX
  AP <--> MEM
  ORCH --> ART
  ORCH --> AUDIT
  ORCH --> META
  CICD --> ART
```

### Planos da plataforma

1. **Experience & Integration:** GitHub, portal, ChatOps e pipelines são os pontos de entrada, nunca credenciais diretas para modelos ou ferramentas.
2. **Agent Control Plane:** mantém workflows duráveis, catálogo versionado, políticas, avaliações, budgets e aprovações.
3. **Agent Plane:** cada agente possui identidade, prompt, modelo, ferramentas, budget e escopo próprios.
4. **Knowledge & Data Plane:** memória segregada por projeto, evidências imutáveis, auditoria e grafo de rastreabilidade.
5. **Execution Plane:** todo efeito colateral passa pelo MCP Gateway; execução de código ocorre em sandbox efêmero, sem segredo persistente.

Veja a descrição completa em [`docs/architecture.md`](docs/architecture.md) e as decisões em [`docs/adr/`](docs/adr/).

## Controles essenciais

- **Human-in-the-loop:** aprovação obrigatória para mudança de alto risco, produção, exceção de política e ação destrutiva.
- **Least privilege:** tokens de curta duração vinculados à identidade do agente, projeto, tarefa e ferramenta.
- **Policy-as-code:** decisão central antes de tool calls e novamente nos gates de pipeline; exemplo em [`policies/agent_authorization.rego`](policies/agent_authorization.rego).
- **Isolamento:** worktree/container efêmero, rede deny-by-default, filesystem restrito, limites de CPU/memória/tempo e egress allowlist.
- **Supply chain:** commits e artefatos assinados, SBOM, proveniência e promoção do mesmo digest entre ambientes.
- **Memória segura:** namespaces por tenant/projeto, classificação de dados, retenção, fontes citadas e proteção contra prompt injection.
- **Mudança segura:** canary/progressive delivery, error budget, kill switch, rollback testado e blast radius explícito.
- **FinOps:** limite por execução/projeto e atribuição de custo e tokens ao `change_id`. Roteamento de modelo por risco/qualidade e política de FinOps corporativa seguem o [FinOps Platform](https://github.com/leandrosflora/enterprise-ai-platform-reference-architecture/blob/main/docs/domains/finops-platform.md) e o [Model Selection Framework](https://github.com/leandrosflora/enterprise-ai-platform-reference-architecture/blob/main/docs/architecture/model-selection-framework.md) do repositório de plataforma.

## Contratos e rastreabilidade

O contrato mínimo de uma mudança está em [`contracts/change-envelope.schema.json`](contracts/change-envelope.schema.json). Um `change_id` acompanha todos os eventos e relaciona:

```text
requirement → acceptance criteria → ADR/contract → commit/PR → test/security evidence
            → human approval → artifact digest → deployment → telemetry/incident
```

Eventos usam o envelope em [`contracts/agent-event.schema.json`](contracts/agent-event.schema.json), incluindo identidade, correlação, custo, tokens, decisão de política e referências de evidência.

Versionamento e compatibilidade de contrato (SemVer, major imutável, sem remoção de campo dentro do mesmo major) seguem a convenção de [Contratos de Eventos](https://github.com/leandrosflora/enterprise-ai-platform-reference-architecture/blob/main/docs/contracts/events.md) do repositório de plataforma; este repositório não redefine a política, apenas a aplica aos schemas de `contracts/`.

## Métricas

| Dimensão | Métricas principais |
|---|---|
| Flow | lead time, cycle time, tempo por gate, WIP |
| Qualidade | retrabalho, defeitos escapados, precisão dos testes gerados, mutation score |
| Governança | taxa de aprovação humana, alterações rejeitadas, violações e exceções de política |
| Confiabilidade | change failure rate, MTTR, rollback rate, blast radius |
| Agentes | task success, groundedness, tool-call success, percentual da entrega executado por agentes |
| FinOps | custo e tokens por mudança/agente/etapa, budget excedido, cache hit rate |

As fórmulas e dimensões obrigatórias estão em [`docs/metrics.md`](docs/metrics.md).

## Estrutura do repositório

```text
.
├── contracts/                 # schemas de eventos e mudanças
├── docs/
│   ├── adr/                   # decisões arquiteturais
│   ├── architecture.md        # componentes, fluxos e deployment
│   ├── governance.md          # papéis, gates e autorização
│   ├── metrics.md             # SLOs e métricas
│   └── threat-model.md        # ameaças e controles
├── examples/                  # workflow, change envelope e trilhas de eventos (aprovado, rejeitado, rollback), validáveis contra os schemas
├── policies/                  # policy-as-code (OPA/Rego)
└── scripts/                   # validação local sem dependências externas
```

## Validação local

```bash
python3 scripts/validate.py
```

O validador verifica JSON Schemas, exemplos, referências de agentes e invariantes de segregação de funções sem depender de pacotes externos.

## Roadmap de adoção

1. **Assistido:** Product, Architecture e Developer geram propostas; humanos executam e aprovam.
2. **Governado:** MCP Gateway, identidades, evidence bundles, policies e avaliações bloqueantes.
3. **Automatizado:** agentes executam mudanças de baixo risco em sandboxes e abrem PRs.
4. **Progressivo:** Release Agent promove automaticamente canários dentro de budgets e SLOs.
5. **Adaptativo:** feedback de produção melhora avaliações e memória, sem autoalterar políticas ou prompts promovidos.

Autonomia é concedida por **classe de risco e evidência observada**, nunca apenas por capacidade do modelo.
