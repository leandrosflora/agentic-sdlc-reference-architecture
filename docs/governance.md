# Governança, autorização e gates

## Modelo de risco

| Classe | Exemplo | Autonomia máxima | Aprovação |
|---|---|---|---|
| R0 | consulta e resumo sem dado restrito | automática | não |
| R1 | documentação ou teste isolado | PR automático | revisão normal |
| R2 | código de aplicação reversível | sandbox + PR | owner independente |
| R3 | schema, IAM, rede ou dado sensível | proposta e validação | dois aprovadores, incluindo especialista |
| R4 | produção destrutiva/irreversível | diagnóstico somente | change authority + execução humana |

O risco é recalculado quando o diff, dependências, dados tocados ou blast radius mudam. O maior risco observado prevalece.

## Matriz de capacidades

| Capacidade | Product | Architecture | Developer | Test | Security | Reviewer | Release | Incident |
|---|:---:|:---:|:---:|:---:|:---:|:---:|:---:|:---:|
| Ler contexto do projeto | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ |
| Alterar requisitos | ✓ | – | – | – | – | comentário | – | comentário |
| Alterar arquitetura/contratos | – | ✓ | proposta | – | comentário | comentário | – | – |
| Escrever código em branch | – | – | ✓ | testes | correção separada | – | – | hotfix proposto |
| Emitir parecer independente | – | – | – | testes | segurança | ✓ | – | – |
| Aprovar a própria saída | – | – | – | – | – | – | – | – |
| Publicar artefato | – | – | – | – | – | – | CI apenas | – |
| Acionar deploy não produtivo | – | – | – | – | – | – | ✓ | – |
| Acionar deploy produtivo | – | – | – | – | – | – | após gate | rollback após gate |

## Gates obrigatórios

1. **Definition gate:** requisito, critérios verificáveis, owner, dados, risco e `change_id`.
2. **Design gate:** ADR quando aplicável, contratos compatíveis, threat model e plano de rollback.
3. **Build gate:** diff dentro do escopo, commit assinado, licenças permitidas e SBOM.
4. **Verification gate:** testes determinísticos, cobertura de critérios, mutation/quality thresholds e evidências reproduzíveis.
5. **Security gate:** secrets, SAST, SCA, IaC e container scan; achados acima do limite bloqueiam.
6. **Approval gate:** aprovador humano independente, MFA, escopo/digest explícitos e validade temporal.
7. **Release gate:** mesmo artifact digest aprovado, janela válida, health checks, capacidade de rollback e error budget.
8. **Observation gate:** canary saudável durante a janela e ausência de regressão nos SLOs.

Exceções são temporárias, justificadas, vinculadas a owner e data de expiração e nunca são aprovadas pelo agente solicitante.

## Invariantes de autorização

- Default deny; permissões são capacidades explícitas, não papéis genéricos.
- Agentes não recebem credenciais humanas ou secrets no prompt.
- `actor_id`, `agent_id`, `workflow_id`, `project_id` e `change_id` devem concordar com o token e o recurso.
- Escrita em produção requer artefato imutável, aprovação humana válida e política vigente.
- Autor e aprovador de uma alteração não podem ser a mesma identidade nem instâncias do mesmo papel delegado.
- Aprovação é invalidada se digest, escopo, risco ou evidence bundle mudar.
- Break-glass é humano, time-bound, alertado e revisado posteriormente.

## Aprovação humana útil

A interface apresenta requisito, diff semântico, decisões arquiteturais, risco, achados, testes, custo, blast radius e rollback. Evita “rubber stamping” ao exigir uma decisão sobre escopo/digest específicos, registrar tempo e justificativa e amostrar aprovações para auditoria de qualidade.
