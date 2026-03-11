---
id: F10-run-report-one-real-adapter
type: feature
summary: Fechar o MVP com geracao de RUN_REPORT.md e integracao minima do Codex CLI como primeiro adapter real do AIgnt-Synapse-Flow.
inputs:
  - CONTEXT.md
  - docs/architecture/SDD.md
  - docs/architecture/TDD.md
  - docs/architecture/SPEC_FORMAT.md
  - features/F09-supervisor-mvp/SPEC.md
outputs:
  - run_report_generator
  - codex_cli_adapter
  - pipeline_document_step
  - report_and_adapter_tests
constraints:
  - manter o AIgnt-Synapse-Flow como engine propria de pipeline do AIgnt OS
  - manter o recorte em um unico adapter real
  - reutilizar o fluxo container-first ja existente via ./scripts/dev-codex.sh
  - nao introduzir novos adapters reais, scheduler complexo ou CLI publica adicional nesta feature
  - manter DOCUMENT como etapa deterministica local, sem delegar sua geracao a um agente externo
acceptance_criteria:
  - Existe um gerador deterministico de `RUN_REPORT.md` a partir de run, steps, eventos e artefatos persistidos.
  - O `PipelineEngine` suporta execucao ate `DOCUMENT`.
  - O `RUN_REPORT.md` e salvo em `artifacts/<run_id>/RUN_REPORT.md` ao concluir uma run persistida ate `DOCUMENT`.
  - A persistencia registra metadados minimos de execucao por step para uso do relatorio, incluindo ferramenta, return code, duracao e timeout quando disponiveis.
  - Existe um `CodexCLIAdapter` concreto que encapsula a execucao nao interativa do Codex via `./scripts/dev-codex.sh -- exec`.
  - Existe pelo menos um teste unitario cobrindo a montagem do comando do `CodexCLIAdapter`.
  - Existe pelo menos um teste de integracao cobrindo uma run persistida ate `DOCUMENT` com geracao de `RUN_REPORT.md`.
non_goals:
  - adicionar segundo adapter real
  - mudar a heuristica do supervisor
  - retomar retries entre polls do worker
  - criar nova CLI publica para consultar runs ou relatorios
dependencies:
  - F09-supervisor-mvp
---

# Contexto

Depois da F09, o AIgnt-Synapse-Flow, a engine propria de pipeline do AIgnt OS, ja consegue executar a run linear ate `SECURITY` com retry e rework deterministico. O gap restante do MVP esta no fechamento auditavel da run e na prova de que o runtime realmente consegue integrar pelo menos uma ferramenta externa de forma controlada.

O repositório ja tem a fixture de `RUN_REPORT.md`, o launcher container-first `./scripts/dev-codex.sh` e a base abstrata para adapters CLI. Falta conectar essas peças ao fluxo persistido, expandir a pipeline ate `DOCUMENT` e materializar um caminho minimo de ponta a ponta com um adapter real.

# Objetivo

Entregar o fechamento do MVP com duas capacidades finais e acopladas de forma minima:

- gerar `RUN_REPORT.md` deterministico ao final da run persistida;
- integrar o `CodexCLIAdapter` como primeiro adapter real do projeto;
- expandir a pipeline de `SECURITY` para `DOCUMENT` e manter o fluxo auditavel;
- registrar metadados suficientes por step para relatar ferramenta usada, codigo de retorno, duracao e timeout quando existirem.

# Escopo

## Incluido

- gerador local de `RUN_REPORT.md`
- persistencia de metadados minimos de execucao por step
- etapa `DOCUMENT` na pipeline e no runner persistido
- `CodexCLIAdapter` concreto usando `./scripts/dev-codex.sh -- exec`
- testes unitarios, de pipeline e de integracao do recorte

## Fora de escopo

- adapter real adicional alem do Codex
- parsing rico do output do Codex alem do necessario para hand-off textual minimo
- validacao pratica obrigatoria com Docker/runtime completo em toda execucao de teste
- mudanca de CLI publica para listar ou baixar relatorios

# Requisitos funcionais

1. O sistema deve conseguir executar uma run persistida ate `DOCUMENT`.
2. O sistema deve gerar um `RUN_REPORT.md` deterministico a partir dos dados persistidos da run.
3. O sistema deve salvar o relatorio final em `artifacts/<run_id>/RUN_REPORT.md`.
4. O sistema deve registrar por step, quando disponivel, `tool_name`, `return_code`, `duration_ms` e `timed_out`.
5. O `CodexCLIAdapter` deve construir a chamada nao interativa via `./scripts/dev-codex.sh -- exec`.
6. O adapter deve produzir um `CLIExecutionResult` compativel com o contrato ja existente.
7. O pipeline nao deve depender do adapter real para gerar `RUN_REPORT.md`; o relatorio deve funcionar tambem com executores locais.

# Requisitos nao funcionais

- O relatorio deve ser deterministicamente ordenado.
- `DOCUMENT` deve continuar sendo um passo local e pequeno.
- O adapter real deve continuar sem shell e sem montagem dinamica insegura de comando.
- A feature deve preservar compatibilidade com os modos sync e async ja existentes.

# Casos de erro

- run inexistente ao tentar gerar o relatorio
- step sem metadados de ferramenta
- falha de escrita do `RUN_REPORT.md`
- execucao do Codex com return code nao zero
- timeout do subprocesso do adapter real

# Cenarios verificaveis

## Cenario 1: run persistida gera relatorio final

- Dado uma run valida executada ate `DOCUMENT`
- Quando a etapa `DOCUMENT` concluir
- Entao existe `artifacts/<run_id>/RUN_REPORT.md`
- E o relatorio resume estados, ferramentas, falhas e artefatos

## Cenario 2: metadados de ferramenta aparecem no relatorio

- Dado um step executado por adapter real
- Quando a run conclui ate `DOCUMENT`
- Entao o relatorio mostra a ferramenta usada, return code e duracao do step

## Cenario 3: adapter real do Codex monta comando seguro

- Dado um prompt textual
- Quando o `CodexCLIAdapter` construir seu comando
- Entao a chamada usa `./scripts/dev-codex.sh -- exec`
- E nao depende de shell

# Observacoes

Esta feature fecha o MVP demonstravel. Se a validacao pratica do `CodexCLIAdapter` encontrar bloqueio operacional real no launcher container-first, a mitigacao aceita neste recorte e manter o adapter coberto por testes controlados e tratar o ajuste operacional como follow-up separado.
