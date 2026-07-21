# ADR 0001 — Orquestração durável centralizada

- Status: aceita
- Data: 2026-07-21

## Contexto

O fluxo cruza agentes, pessoas e sistemas, pode durar dias e precisa sobreviver a falhas sem duplicar efeitos.

## Decisão

Usar um orquestrador durável como autoridade do estado. Agentes são workers stateless: recebem uma tarefa limitada, devolvem saída estruturada e não escolhem unilateralmente a próxima etapa. Side effects usam idempotency keys e compensações explícitas.

## Consequências

Há rastreabilidade, retomada, timeout e intervenção humana consistentes. Em contrapartida, workflows e migrações de estado precisam ser versionados, e o control plane torna-se componente crítico.
