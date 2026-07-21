# Topologia de deployment

Os agentes não executam dentro de Jira, GitHub, Azure DevOps ou IDEs. Essas ferramentas disparam workflows e exibem resultados; a execução ocorre na plataforma corporativa.

~~~mermaid
flowchart TB
  subgraph EXP["Experience zone"]
    SCM["SCM e work management"]
    IDE["IDE"]
    PORTAL["Developer Portal e ChatOps"]
  end
  subgraph CTRL["Control plane — cluster dedicado"]
    API["Workflow API"]
    ORCH["Orquestrador durável"]
    GOV["Registry, Policy, Evaluation e Cost"]
    DATA["Workflow DB e audit refs"]
  end
  subgraph EXEC["Execution plane — trust zones isoladas"]
    WORK["Agent workers efêmeros"]
    SBX["Sandboxes de código"]
    MCP["MCP Gateway"]
  end
  subgraph EXT["Serviços corporativos"]
    MODEL["Model providers"]
    TOOLS["SDLC tools"]
    STORE["Artifact, evidence e telemetry"]
  end
  SCM --> API
  IDE --> API
  PORTAL --> API
  API --> ORCH
  ORCH --> GOV
  ORCH --> DATA
  ORCH --> WORK
  WORK --> MODEL
  WORK --> MCP
  WORK --> SBX
  MCP --> TOOLS
  SBX --> STORE
  ORCH --> STORE
~~~

## Unidades de implantação

| Unidade | Ciclo de vida | Escala | Acesso |
|---|---|---|---|
| Workflow API | persistente | webhooks e requisições | control plane |
| Orquestrador | persistente, multi-AZ | workflows ativos | metadados, filas e policies |
| Registry/PDP/Evaluation | persistente | decisões e avaliações | definições versionadas |
| Agent worker | efêmero por etapa | papel, fila e risco | modelo, memória autorizada e MCP |
| Code sandbox | efêmero por tentativa | CPU, memória e concorrência | checkout, build e egress allowlist |
| Release executor | pipeline corporativo | ambientes e janelas | artefato por digest |
| Incident worker | efêmero, read-only | eventos operacionais | telemetria autorizada |

## Trust zones

- **Control plane:** não executa código gerado.
- **Non-production execution:** workers e sandboxes não acessam produção.
- **Production delivery:** somente pipeline corporativo promove o digest aprovado.
- **Audit domain:** administração separada e armazenamento append-only/WORM.
- **Model provider:** recebe apenas contexto mínimo, classificado e sanitizado.

Cada execução recebe workload identity vinculada a agent, project, change e audiência. Tokens têm TTL menor que a tarefa. Egress é deny-by-default. Segredos são obtidos just-in-time e nunca entram no prompt.

O control plane opera multi-AZ e faz checkpoint antes e depois de side effects. Workers são descartáveis. Escritas falham fechadas sem policy, identidade ou auditoria. A indisponibilidade dos agentes não impede rollback humano pelo pipeline.
