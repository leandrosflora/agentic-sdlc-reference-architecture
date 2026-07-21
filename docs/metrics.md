# Métricas e avaliações

Todas as métricas são segmentadas por projeto, tipo e classe de risco, workflow version, agente/modelo/prompt version e período. Comparações sem esses recortes podem mascarar seleção de tarefas.

| Métrica | Definição operacional |
|---|---|
| Lead time | `produção concluída - requisito aceito` |
| Cycle time | `primeiro trabalho ativo - produção concluída`, excluindo fila explicitamente |
| Retrabalho | mudanças que retornam a etapa anterior / mudanças iniciadas |
| Defeitos escapados | defeitos ligados à mudança encontrados após produção / mudanças publicadas |
| Aprovação humana | aprovações / decisões humanas; medir também latência e reversões |
| Custo por mudança | modelo + ferramentas + compute + armazenamento atribuídos ao `change_id` |
| Alterações rejeitadas | PRs ou gates rejeitados / alterações propostas, por motivo |
| Precisão dos testes | testes gerados que detectam mutantes/defeitos relevantes / testes gerados válidos |
| MTTR | média de `incidente detectado → serviço restaurado` |
| Execução por agentes | etapas concluídas por agentes / etapas elegíveis; não usar linhas de código |
| Change failure rate | deploys que causam incidente, rollback ou hotfix / deploys |
| Task success | execuções que atendem critérios verificáveis / execuções iniciadas |

## SLOs da plataforma

- Disponibilidade do control plane e latência p95 por operação.
- Taxa de conclusão de workflows e tempo bloqueado por dependência.
- Tool calls permitidas, negadas, com erro e repetidas.
- Falhas de correlação, eventos sem evidência e divergência de artifact digest.
- Consumo de tokens/custo versus budget e desperdício por retry.
- Incidentes de segurança, tentativa de exfiltração e policy denials.

## Avaliação de agentes

1. **Offline:** golden tasks versionadas, casos adversariais, prompt injection, tool misuse, precisão e custo.
2. **Pre-production:** shadow mode e sandbox com dados sintéticos; nenhuma escrita real.
3. **Online:** canary por classe de risco, guardrails determinísticos e amostragem humana.
4. **Contínua:** drift por modelo/prompt/ferramenta, regressão após incidentes e comparação com baseline humano.

Uma avaliação registra dataset digest, versões, seed/configuração, resultado por caso, avaliador, custo e evidências. Métricas baseadas em LLM são calibradas contra humanos e acompanhadas de falsos positivos/negativos.

## Telemetria mínima por evento

`timestamp`, `trace_id`, `change_id`, `project_id`, `workflow_id/version`, `agent_id/version`, `model`, `prompt_digest`, `tool`, `policy_decision`, tokens, custo, duração, retry, estado, evidence refs e outcome. Conteúdo sensível não é label de métrica e deve ser redigido em logs.
