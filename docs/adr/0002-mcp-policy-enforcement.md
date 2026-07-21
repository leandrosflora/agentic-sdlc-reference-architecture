# ADR 0002 — MCP Gateway como ponto de enforcement

- Status: aceita
- Data: 2026-07-21

## Contexto

Permitir que agentes chamem APIs diretamente espalha credenciais, auditoria e regras de autorização e amplia o impacto de prompt injection.

## Decisão

Toda ferramenta corporativa acessível por agente é publicada por um MCP Gateway governado. O gateway autentica workload e workflow, valida schemas, consulta policy-as-code, aplica limites, sanitiza dados e registra evidências. Credenciais downstream são trocadas just-in-time e não ficam visíveis ao modelo.

## Consequências

Obtemos uma fronteira consistente para autorização e auditoria, mas o gateway precisa de alta disponibilidade, isolamento por trust zone e catálogo de ferramentas cuidadosamente mantido.
