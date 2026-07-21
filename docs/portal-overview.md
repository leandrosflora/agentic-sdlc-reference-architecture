# Portal operacional

O portal mínimo está publicado junto ao MkDocs em **/portal/**. Ele não substitui Jira, Azure Boards ou GitHub: consolida o estado que fica disperso entre essas ferramentas.

[Abra o dashboard](portal/index.html){ .md-button .md-button--primary }

## Visões disponíveis

- identidade da mudança, projeto, risco e estado;
- progresso por etapa e agente;
- custo total e por etapa;
- evidências e hashes;
- Change Set e quantidade de repositórios;
- links para o sistema de registro.

## Evolução para Backstage

O portal usa um contrato JSON independente de framework. Em uma adoção corporativa, a mesma API pode alimentar um plugin Backstage com cards na entidade Component ou System. O portal mínimo evita tornar Backstage uma dependência obrigatória desta referência.
