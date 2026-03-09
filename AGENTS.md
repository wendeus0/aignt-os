# AGENTS.md

## Objetivo do repositório
Este repositório implementa o AIgnt OS, um meta-orquestrador de agentes de IA via CLI.
A implementação deve seguir a arquitetura e decisões já documentadas, sem reinventar o projeto a cada feature.

## Fontes de verdade
Antes de iniciar qualquer trabalho, leia nesta ordem:
1. `CONTEXT.md`
2. `docs/architecture/SDD.md`
3. `docs/architecture/TDD.md`
4. `docs/architecture/SPEC_FORMAT.md`
5. `features/<feature>/SPEC.md` da feature atual

Em caso de conflito:
- `SPEC.md` da feature governa o comportamento da feature
- `SDD.md` governa a arquitetura
- `TDD.md` governa a estratégia de implementação e testes
- `SPEC_FORMAT.md` governa o formato da SPEC

## Regras gerais
- Trabalhe **uma feature por vez**.
- Não misture escopo de duas features na mesma mudança.
- Sempre siga a ordem:
  1. refinar o pedido do usuário em SPEC
  2. criar testes RED
  3. implementar o código mínimo GREEN
  4. refatorar sem quebrar os testes
  5. atualizar o relatório da feature
- Nunca invente requisitos ausentes. Se faltar informação, reduza escopo e registre a lacuna em `NOTES.md`.
- Prefira mudanças pequenas, localizadas e reversíveis.
- Nunca altere docs centrais sem necessidade real da feature.
- Use sempre a expressão **engine própria de pipeline** ao se referir ao runtime interno do AIgnt OS.
- Preserve o caráter **CLI-first**, **spec-first** e **feature-by-feature** do projeto.

## Escopo do MVP
No MVP:
- 1 workspace por run
- memória semântica apenas advisory/read-only
- observabilidade local
- `RUN_REPORT.md` por execução
- pipeline linear state-driven
- runtime dual simples: CLI efêmero + worker leve
- sem DAG distribuída real
- sem vector DB obrigatório
- sem roteamento automático por memória semântica

## Critérios de parada
Pare imediatamente e peça revisão quando:
- a `SPEC.md` estiver ambígua
- os testes contradisserem a SPEC
- a mudança exigir refatoração ampla fora da feature
- a mudança pedir alteração arquitetural não coberta pelos ADRs
- a saída esperada não puder ser validada de forma clara

## Política de desenvolvimento
- Faça TDD de forma explícita.
- Escreva testes antes do código de produção.
- Não refatore antes de os testes ficarem verdes.
- Mantenha baixo acoplamento e contratos explícitos com Pydantic.
- Trate parsing como componente crítico.
- Separe output bruto de output limpo.
- Não use abstrações prematuras.

## Agentes recomendados
### 1. spec-editor
Responsável por:
- melhorar o pedido do usuário
- transformar o pedido em `SPEC.md`
- ajustar `SPEC_FORMAT.md` apenas se necessário
- reduzir ambiguidade
Não implementa código de produção.

### 2. test-red
Responsável por:
- ler `SPEC.md`
- criar testes que falham
- validar critérios de aceite da feature
Não implementa código de produção.

### 3. green-refactor
Responsável por:
- implementar o mínimo para passar nos testes
- refatorar após os testes ficarem verdes
- manter compatibilidade com a arquitetura
Não altera a SPEC sem motivo explícito.

## Alternativas de operação
Se multi-agent não estiver disponível:
- execute `spec-editor` primeiro
- depois `test-red`
- depois `green-refactor`

Se multi-agent estiver disponível:
- `spec-editor` roda primeiro
- `test-red` e leituras auxiliares podem rodar em paralelo apenas quando a SPEC estiver estável
- `green-refactor` só começa após a etapa RED estar validada

## Entregáveis por feature
Cada feature deve terminar com:
- `SPEC.md` atualizado
- testes cobrindo a feature
- implementação mínima funcional
- refatoração concluída
- `NOTES.md` com decisões locais
- checklist de aceite da feature
