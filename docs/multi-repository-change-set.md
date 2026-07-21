# Change Set multi-repositório

Um Change Set agrupa alterações correlacionadas em vários repositórios sob o mesmo change_id. Cada repository change mantém branch, componente, dependências, evidências e artifact digest próprios.

## Regras

- o risco do Change Set é o maior risco de seus itens;
- dependências formam um grafo acíclico;
- todos os PRs devem referenciar change_set_id e change_id;
- contratos compartilhados são validados antes dos consumidores;
- aprovação é vinculada ao conjunto de digests;
- alteração de qualquer digest invalida a aprovação do conjunto;
- deployment segue ordem topológica;
- rollback segue ordem reversa ou plano coordenado explícito;
- conclusão parcial precisa ser estado visível, nunca sucesso implícito.

~~~mermaid
flowchart TB
  C["CSET-1001"]
  C --> API["API"]
  C --> WEB["Frontend"]
  C --> INFRA["Deployment"]
  API --> WEB
  WEB --> INFRA
~~~

O schema está em [change-set.schema.json](https://github.com/leandrosflora/agentic-sdlc-reference-architecture/blob/main/contracts/change-set.schema.json) e o exemplo em [change-set.instance.json](https://github.com/leandrosflora/agentic-sdlc-reference-architecture/blob/main/examples/change-set.instance.json).

## Estratégias

| Estratégia | Uso | Regra |
|---|---|---|
| Atomic | componentes inseparáveis | todos promovem ou todos voltam |
| Coordinated | ordem e janela comuns | checkpoints e compensações por etapa |
| Independent | itens reversíveis e desacoplados | falha isolada não invalida itens saudáveis |

Migrações incompatíveis usam expand/contract. O Architecture Agent define dependências e o Release Agent executa o plano aprovado; nenhum deles altera silenciosamente a ordem durante a release.
