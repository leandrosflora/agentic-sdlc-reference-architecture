# Golden path executável

O golden path comprova onboarding, evento canônico, coordenação multi-repositório, gates, aprovação, release, observação e evidências sem chamar LLM ou produção.

~~~bash
python3 scripts/run_golden_path.py
python3 scripts/validate.py
~~~

## Saída consumida pelo portal

A automação gera o arquivo dashboard-data.json a partir da saída do fluxo. O mesmo payload alimenta:

- resumo do GitHub Check;
- comentário atualizado no pull request;
- dashboard de workflow;
- evidências por etapa;
- métricas de custo e execução.

No exemplo, os custos são determinísticos e servem apenas para demonstrar o contrato de visualização.
