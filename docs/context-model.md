# Modelo de contexto

Contexto não é uma conversa longa. É um conjunto versionado, classificado e autorizado de referências montado para cada execução.

## Camadas

| Camada | Conteúdo | Fonte canônica | Escopo e retenção |
|---|---|---|---|
| Institucional | políticas, padrões e controles | repositórios corporativos | organização; versionada |
| Produto | domínio, roadmap, SLOs e ownership | catálogo e work management | produto; ciclo de vida |
| Projeto | arquitetura, ADRs, contratos e runbooks | SCM e portal | projeto; versionada |
| Mudança | requisito, Change Set, diff e evidências | orquestrador e evidence store | change_id; auditável |
| Execução | plano, tool results e scratch state | worker/checkpoint | agent_run_id; efêmera |
| Recuperado | trechos citados e metadados | Project Memory | tarefa; TTL e policy |
| Feedback | telemetria e incidentes em staging | observabilidade | só promove após revisão |

## Context envelope

Cada execução recebe identidade, objetivo, critérios de aceite, risco, capabilities, referências autorizadas, budgets e hashes de versões. Conteúdo recuperado inclui source URI, digest, classificação, validade e timestamp.

## Precedência

1. policy e system instructions promovidas;
2. workflow e Agent Definition versionados;
3. requisito e aprovação válidos;
4. fontes institucionais e de projeto;
5. tool results;
6. conteúdo externo não confiável.

Uma fonte inferior nunca substitui política ou autorização. Conflitos são registrados e encaminhados ao owner.

## Montagem e minimização

O Context Builder consulta o Project Memory com identidade de workload e filtros por tenant, projeto, classificação e finalidade. Seleciona apenas trechos necessários, respeita token budget e preserva citações. Secrets, dados fora do escopo e conteúdo sem proveniência não entram no prompt.

~~~mermaid
flowchart LR
  S["Fontes versionadas"] --> B["Context Builder"]
  I["Identity e policy"] --> B
  B --> F["Filtro, ranking e redaction"]
  F --> E["Context envelope"]
  E --> W["Agent worker"]
  W --> A["Evidence e audit"]
~~~

## Atualização e proteção

Saídas de agentes e telemetria entram em staging. Promoção exige sanitização, deduplicação, verificação de origem, avaliação e aprovação do owner. Namespaces impedem recuperação cross-project. Conteúdo externo é delimitado como dado não confiável e nunca concede tools.
