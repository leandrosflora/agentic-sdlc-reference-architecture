# Threat model

## Ativos e fronteiras de confiança

Ativos principais: código, propriedade intelectual, credenciais, dados de clientes, memória, prompts, políticas, evidence bundles, artefatos, pipelines e telemetria. As fronteiras ficam entre usuário/integração, control plane, provedor de modelo, MCP/tools, sandboxes, data plane e produção.

| Ameaça | Cenário | Controles preventivos/detectivos |
|---|---|---|
| Prompt injection | issue, código, log ou página instrui o agente a ignorar controles | conteúdo não confiável delimitado, tool policy externa ao modelo, allowlist, detecção e avaliação adversarial |
| Exfiltração | contexto/segredo enviado ao modelo ou domínio externo | classificação, DLP, egress proxy, secrets fora do prompt, redaction e modelos aprovados |
| Confused deputy | agente usa sua autoridade para pedido de outro projeto | identidade vinculada a tarefa/projeto/recurso, autorização por chamada e audience restrita |
| Supply-chain compromise | dependência, MCP server ou imagem maliciosa | pin por digest, assinatura, SBOM, provenance, scan, catálogo aprovado e isolamento |
| Memory poisoning | saída falsa vira conhecimento confiável | proveniência, staging, aprovação, expiração, namespace e imutabilidade da fonte |
| Unauthorized change | agente altera escopo, política, pipeline ou produção | protected paths/branches, SoD, policy-as-code, digest-bound approval e default deny |
| Sandbox escape | código gerado acessa host/rede/metadata | microVM/container hardened, rootless, seccomp, quotas, egress deny e runner descartável |
| Audit tampering | agente apaga ou fabrica evidência | append-only/WORM, hash/assinatura, storage e administração separados |
| Denial of wallet | loops, contexto enorme ou retries geram custo | budgets hierárquicos, max steps/tokens, timeout, circuit breaker e alertas |
| Unsafe incident action | diagnóstico incorreto amplia incidente | Incident Agent read-only por padrão, runbooks aprovados, blast radius e confirmação humana |

## Abuso e resposta

Sinais de abuso incluem chamadas fora da sequência, tentativas repetidas negadas, crescimento anormal de tokens, recuperação cross-project e divergência entre aprovação e digest. A resposta pode revogar identidade, desabilitar agente/ferramenta, congelar workflow, preservar evidências e acionar o processo de incidente.

## Blast radius e rollback

Toda release declara recursos/tenants/regiões afetados, concorrência, percentual inicial, SLOs e condição automática de parada. Rollback usa o digest anterior conhecido, é testado antes da promoção e não depende do agente/modelo que originou a mudança. Migrações irreversíveis exigem estratégia expand/contract e aprovação R3/R4.
