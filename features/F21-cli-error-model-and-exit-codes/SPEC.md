---
id: F21-cli-error-model-and-exit-codes
type: feature
summary: Organizar categorias de erro e exit codes previsiveis para a CLI publica do SynapseOS.
inputs:
  - CONTEXT.md
  - docs/architecture/SDD.md
  - docs/architecture/TDD.md
  - docs/architecture/SPEC_FORMAT.md
  - docs/architecture/PHASE_2_ROADMAP.md
  - src/synapse_os/cli/app.py
  - tests/integration/test_runtime_cli.py
  - tests/integration/test_runs_cli.py
  - tests/integration/test_runs_submit_cli.py
outputs:
  - cli_error_contract
  - cli_error_tests
  - feature_notes_and_checklist
constraints:
  - manter o Synapse-Flow como a engine propria de pipeline do SynapseOS
  - manter o recorte restrito ao contrato de erro da CLI publica atual
  - nao introduzir novos subcomandos, novo modo verbose nem debug profundo
  - preservar os caminhos de sucesso existentes com exit code `0`
  - nao alterar schema SQLite, worker, pipeline ou artifacts
  - nao exigir DOCKER_PREFLIGHT, pois a frente nao depende de validacao pratica em Docker
acceptance_criteria:
  - "A CLI publica passa a usar um contrato previsivel de exit codes: `0` sucesso, `2` uso invalido, `3` recurso ausente, `4` validacao de entrada, `5` erro de ambiente/precondicao e `6` erro de execucao inesperada."
  - "Erros de `runs submit` e `runs show` retornam mensagens sem traceback cru, com prefixo estavel por categoria."
  - "Erros operacionais de `runtime start|status|ready|stop` retornam mensagens sem traceback cru, com prefixo estavel por categoria."
  - "Existe pelo menos um teste de integracao cobrindo cada categoria publica de erro usada por `runs` e `runtime`, com verificacao explicita do exit code."
  - "A ajuda e os parse errors nativos do Typer permanecem funcionando com exit code `2`."
non_goals:
  - adicionar modo verbose ou debug detalhado
  - mudar rendering de sucesso
  - introduzir nova taxonomia de erro no runtime interno ou na pipeline
  - implementar preview de artifacts
security_notes:
  - manter mensagens de erro sem traceback cru e sem vazamento de segredo ou conteudo de artifacts
  - nao adicionar shell, subprocesso ou leitura nova de arquivo
dependencies:
  - F15-public-run-submission
  - F16-run-detail-expansion
---

# Contexto

A CLI publica do SynapseOS ja expõe `runs submit`, `runs show` e o grupo `runtime`, enquanto o Synapse-Flow continua como a engine propria de pipeline do SynapseOS. Porem, os caminhos de falha ainda usam uma mistura de `typer.BadParameter`, `typer.Exit(code=1)` e mensagens ad hoc, o que dificulta automacoes e torna os erros menos previsiveis para operadores.

A etapa 2 prioriza endurecer o contrato operacional da CLI antes de consolidar o caminho canonico de demonstracao. A F21 existe para transformar falhas recorrentes em um modelo pequeno, legivel e testavel.

# Objetivo

Entregar um contrato publico de erro para a CLI, com categorias e exit codes previsiveis, cobrindo os comandos publicos atuais sem alterar seus caminhos de sucesso.

# Escopo

## Incluido

- contrato centralizado de exit codes da CLI
- mensagens de erro com prefixo estavel por categoria
- padronizacao dos erros de `runs submit`, `runs show` e `runtime start|status|ready|stop`
- testes unitarios e de integracao para os codigos de erro
- notes e checklist proprios da feature

## Fora de escopo

- novo subcomando de debug
- verbose mode ou stack traces sob opt-in
- mudancas em pipeline, persistencia, worker ou preview de artifacts
- taxonomia completa de erros para adapters reais

# Requisitos funcionais

1. A CLI deve expor o seguinte contrato de exit codes:
   - `0` sucesso
   - `2` uso invalido
   - `3` recurso ausente
   - `4` validacao de entrada
   - `5` erro de ambiente/precondicao
   - `6` erro de execucao inesperada
2. As mensagens de erro da aplicacao devem usar prefixo estavel:
   - `Usage error:`
   - `Not found:`
   - `Validation error:`
   - `Environment error:`
   - `Execution error:`
3. `runs show <run_id>` com run ausente deve retornar `3`.
4. `runs submit <spec_path>` com `SPEC` ausente deve retornar `3`.
5. `runs submit <spec_path>` com `SPEC` invalida deve retornar `4`.
6. `runs submit` com `--mode` ou `--stop-at` invalido deve retornar `2`.
7. `runtime ready`, `runtime stop`, `runtime start` duplicado e `runtime status` inconsistente devem retornar `5`.
8. Falha inesperada de execucao em caminho publico da CLI deve retornar `6`.

# Requisitos nao funcionais

- A implementacao deve ficar concentrada na camada de CLI.
- Os caminhos de sucesso existentes devem permanecer inalterados.
- A ajuda e os parse errors nativos do Typer devem continuar operando com exit code `2`.

# Casos de erro

- `run_id` inexistente
- path de `SPEC` ausente
- `SPEC` invalida
- `mode` invalido
- `stop_at` invalido
- runtime nao pronto
- runtime nao rodando
- runtime ja em execucao
- estado inconsistente do runtime
- falha inesperada em dispatch ou runtime

# Cenarios verificaveis

## Cenario 1: erro de recurso ausente

- Dado um `run_id` inexistente ou uma `SPEC` ausente
- Quando a CLI publica correspondente for executada
- Entao a falha retorna exit code `3`
- E a mensagem usa o prefixo `Not found:`

## Cenario 2: erro de validacao e uso

- Dado uma `SPEC` invalida ou argumentos opcionais invalidos
- Quando `runs submit` for executado
- Entao a `SPEC` invalida retorna `4`
- E o uso invalido retorna `2`

## Cenario 3: erro operacional de ambiente

- Dado um runtime indisponivel, inconsistente ou em estado incompatível
- Quando um comando `runtime` correspondente for executado
- Entao a falha retorna `5`
- E a mensagem usa o prefixo `Environment error:`

## Cenario 4: erro inesperado

- Dado uma falha inesperada em caminho publico da CLI
- Quando o comando for executado
- Entao a falha retorna `6`
- E a mensagem usa o prefixo `Execution error:`

# Observacoes

Esta frente organiza o contrato publico de erro da CLI, mas nao tenta definir toda a taxonomia do runtime interno nem dos adapters. O objetivo e estabilizar a superficie publica atual antes das frentes de happy path, doctor e onboarding.
