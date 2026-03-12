---
id: F14-runs-observability-cli
type: feature
summary: Expor inspeção CLI-first de runs persistidas e seus eventos/artefatos sem abrir uma TUI.
inputs:
  - CONTEXT.md
  - docs/architecture/SDD.md
  - docs/architecture/TDD.md
  - docs/architecture/SPEC_FORMAT.md
  - memory.md
  - PENDING_LOG.md
  - src/aignt_os/cli/app.py
  - src/aignt_os/persistence.py
outputs:
  - runs_cli_commands
  - rich_runs_rendering
  - runs_cli_tests
constraints:
  - manter o AIgnt-Synapse-Flow como a engine propria de pipeline do AIgnt OS
  - manter o recorte limitado a inspecao de runs persistidas ja existentes
  - nao introduzir TUI, Textual, watch mode ou polling continuo
  - reutilizar apenas `RunRepository` e `ArtifactStore` ja existentes
  - nao exigir DOCKER_PREFLIGHT, pois a frente nao depende de validacao pratica em Docker
acceptance_criteria:
  - "`aignt runs list` lista runs persistidas usando a CLI publica e apresenta pelo menos `run_id`, `status` e `current_state`."
  - "`aignt runs show <run_id>` apresenta metadados da run, steps persistidos, eventos persistidos e paths de artefatos quando existirem."
  - "Existe pelo menos um teste de integracao cobrindo `aignt runs list` e pelo menos um teste de integracao cobrindo `aignt runs show <run_id>` contra dados persistidos reais."
  - "Quando o `run_id` nao existir, a CLI retorna falha previsivel sem traceback cru."
  - "A saida enriquecida continua utilizavel em ambiente sem TTY e em captura de testes."
non_goals:
  - criar `aignt tui`
  - adicionar watch mode
  - disparar novas runs pela mesma feature
  - alterar pipeline, worker ou modelo de persistencia
security_notes:
  - limitar a leitura a `runs_db_path` e `artifacts_dir` configurados
  - nao introduzir subprocessos, shell ou leitura arbitraria fora da persistencia ja suportada
dependencies:
  - F07-persistence-artifacts
  - f11-runtime-persistente-minimo
  - F13-rich-cli-output
---

# Contexto

O projeto ja persiste runs, steps, eventos e artefatos locais, e o AIgnt-Synapse-Flow continua como a engine propria de pipeline do AIgnt OS. Porem, a CLI publica ainda expõe apenas comandos de lifecycle do runtime, deixando a observabilidade operacional dependente de leitura manual do banco SQLite e do filesystem.

A proxima janela logica apos a F13 e preencher essa lacuna de observabilidade com baixo risco: primeiro tornar os dados persistidos consultaveis via CLI, e so depois reavaliar uma TUI futura.

# Objetivo

Entregar uma frente pequena e CLI-first para inspecionar runs persistidas, com foco em dois comandos publicos: listagem de runs e visualizacao detalhada de uma run especifica.

# Escopo

## Incluido

- novo grupo publico `aignt runs`
- comando `aignt runs list`
- comando `aignt runs show <run_id>`
- rendering Rich para listagem e detalhe de run
- testes de integracao contra persistencia real
- teste unitario do rendering detalhado em ambiente sem TTY

## Fora de escopo

- TUI com Textual
- watch mode ou streaming de eventos
- criacao de runs pela CLI publica
- mudancas em schema SQLite ou layout de artefatos

# Requisitos funcionais

1. O comando `aignt runs list` deve consultar o repositório configurado e listar as runs persistidas.
2. O comando `aignt runs show <run_id>` deve consultar uma run especifica e exibir:
   - metadados principais da run
   - steps persistidos
   - eventos persistidos
   - paths de artefatos persistidos, quando existirem
3. Quando nao houver runs, `aignt runs list` deve responder de forma legivel e previsivel.
4. Quando o `run_id` nao existir, `aignt runs show <run_id>` deve falhar com mensagem operacional clara.

# Requisitos nao funcionais

- Reutilizar Rich ja presente no projeto.
- Preservar saida assertavel em testes sem depender de ANSI.
- Manter a implementacao localizada na camada de CLI e em helpers de rendering.

# Casos de erro

- base de runs vazia
- `run_id` inexistente
- run sem steps, eventos ou artefatos
- execucao em ambiente nao interativo

# Cenarios verificaveis

## Cenario 1: listagem de runs persistidas

- Dado um repositório com runs persistidas
- Quando `aignt runs list` for executado
- Entao a CLI exibe pelo menos `run_id`, `status` e `current_state`

## Cenario 2: detalhe de run persistida

- Dado uma run persistida com steps, eventos e artefatos
- Quando `aignt runs show <run_id>` for executado
- Entao a CLI exibe os metadados da run
- E exibe os steps persistidos
- E exibe os eventos persistidos
- E exibe os paths de artefatos

## Cenario 3: run ausente

- Dado um `run_id` inexistente
- Quando `aignt runs show <run_id>` for executado
- Entao a CLI falha sem traceback cru
- E informa que a run nao foi encontrada

# Observacoes

Esta frente existe para tornar a observabilidade persistida utilizavel via CLI antes de considerar uma TUI. Qualquer expansao para watch mode, streaming, filtros avancados ou Textual deve ser tratada em feature propria posterior.
