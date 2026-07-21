# Agentic SDLC Reference Architecture

Uma arquitetura de referência para levar agentes além da geração de código e coordenar o fluxo completo entre demanda e produção com identidade, políticas, evidências e aprovação humana.

[Explorar arquitetura](architecture.md){ .md-button .md-button--primary }
[Ver portal operacional](portal/index.html){ .md-button }

## O que esta referência resolve

- agentes especializados do requisito ao feedback de produção;
- núcleo agnóstico com adaptadores para ferramentas do SDLC;
- runtime compartilhado com workers e sandboxes efêmeros;
- segregação entre implementação, revisão, aprovação e release;
- rastreabilidade por change_id e evidence bundle;
- Change Sets com múltiplos repositórios;
- custo, qualidade e risco observáveis por mudança.

## Fluxo de referência

~~~mermaid
flowchart LR
  W["Demanda"] --> P["Product e Architecture"]
  P --> D["Developer"]
  D --> V["Test e Security"]
  V --> A["Review e aprovação"]
  A --> R["Release e observação"]
  R --> W
~~~

## Comece por aqui

1. Entenda a [arquitetura](architecture.md).
2. Veja a [jornada ponta a ponta](change-journey.md).
3. Execute o [golden path](golden-path.md).
4. Abra o [portal operacional](portal/index.html).
