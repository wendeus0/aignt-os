# Test-Driven Development Strategy — AIgnt OS v3

## 1. Objetivo
Definir a estratégia de testes para implementar o AIgnt OS com foco em confiabilidade do **AIgnt-Synapse-Flow**, a engine própria de pipeline do projeto, dos adapters CLI, do formato de SPEC, do runtime dual (CLI + worker leve) e dos hand-offs entre etapas.

## 2. Princípios
- Validar `DOCKER_PREFLIGHT` antes de iniciar execução prática dependente de Docker.
- Testar contratos antes da implementação.
- Separar testes de unidade, integração, pipeline e worker.
- Simular ferramentas CLI com outputs realistas.
- Validar hand-offs entre steps, não apenas comportamento interno.
- Garantir que o AIgnt-Synapse-Flow permaneça refatorável.
- Fazer `TEST_RED` derivar testes da SPEC validada, não do prompt cru.
- Tratar `SECURITY_REVIEW` como gate antes de `REPORT` e `COMMIT`.

---

## 3. Fluxo de execução por feature

```text
SPEC → TEST_RED → CODE_GREEN → REFACTOR → QUALITY_GATE → SECURITY_REVIEW → REPORT → COMMIT
```

- `DOCKER_PREFLIGHT` é executado pela skill `repo-preflight` quando a feature exigir validação prática em Docker.
- O `DOCKER_PREFLIGHT` padrão em CI e no fluxo local deve ser leve, sem `docker compose up`.
- O runtime completo deve ser validado em workflow dedicado ou por acionamento explícito.
- `SECURITY_REVIEW` fecha o ciclo técnico antes de `REPORT` e `COMMIT`.

## 4. Estratégia RED → GREEN → REFACTOR

### RED
Escrever primeiro testes para:
- transições de estado,
- parsing,
- validação da SPEC,
- comportamento dos adapters,
- decisões do supervisor,
- persistência de run,
- comportamento do worker,
- geração do `RUN_REPORT.md`.

### GREEN
Implementar o mínimo necessário para cada contrato passar.

### REFACTOR
Extrair abstrações estáveis:
- `PipelineStep`,
- `StepExecutor`,
- `RunRepository`,
- `SupervisorDecision`,
- `SpecValidator`,
- `ArtifactStore`.

---

## 5. Níveis de Teste

### 5.1 Unit tests
Cobrem:
- limpeza de output,
- extração de blocos,
- validação da SPEC,
- transições da state machine,
- classificação de falhas,
- serialização de modelos,
- geração do `RUN_REPORT.md`,
- validação do `DOCKER_PREFLIGHT`,
- checagens do gate de segurança,
- regras de lock de run.

### 5.2 Integration tests
Cobrem:
- spec engine + schema,
- adapter + parser,
- pipeline manager + supervisor,
- persistência de run,
- CLI + AIgnt-Synapse-Flow,
- worker + repositório de runs.

### 5.3 CLI simulation tests
Simulam subprocessos e ferramentas reais usando `stdout`, `stderr`, `returncode` e timeout falsos.

### 5.4 Pipeline tests
Executam o fluxo ponta a ponta com ambiente fake, incluindo:
- invalidar SPEC,
- reprovar review,
- falhar em security,
- reroute por falha de ferramenta,
- geração de artifacts.

### 5.5 Worker tests
Verificam:
- polling de runs pendentes,
- lock de execução,
- retries longos,
- retomada de run,
- marcação de falha terminal,
- não duplicação de processamento.

### 5.6 Contract tests
Garantem que:
- todos os adapters implementam o contrato mínimo,
- todos os steps devolvem `StepResult` válido,
- toda SPEC válida atende ao schema oficial.

---

## 6. Ordem Recomendada de Implementação
1. SPEC aprovada.
2. Modelos Pydantic principais.
3. Validador da SPEC híbrida.
4. State machine.
5. Cleaner/parser básico.
6. Base adapter async.
7. Step executor.
8. AIgnt-Synapse-Flow linear.
9. Persistência SQLite.
10. Worker leve.
11. Supervisor com retry/reroute.
12. Geração do `RUN_REPORT.md`.
13. Adapters reais.
14. `DOCKER_PREFLIGHT` validado quando a frente exigir execução prática em Docker.
15. Paralelismo controlado.

---

## 7. Estratégia de Mocking
- Mock de subprocess assíncrono.
- Fixtures com stdout realista das ferramentas.
- Snapshots de outputs ruidosos.
- Fixtures para SPEC válida e inválida.
- Repositórios em memória para testes rápidos.
- Artefatos temporários em diretório isolado por teste.

---

## 8. Casos de Teste Prioritários

### 8.1 Preflight e segurança
- `test_docker_preflight_validates_compose_config_without_starting_container()`
- `test_docker_preflight_fails_when_compose_config_is_invalid()`
- `test_security_gate_runs_before_report_and_commit()`
- `test_security_gate_rejects_insecure_operational_patterns()`

### 8.1b Quality gate
- `test_quality_gate_runs_after_refactor_and_before_security_review()`
- `test_quality_gate_blocks_security_when_tests_fail()`
- `test_quality_gate_blocks_security_when_lint_fails()`
- `test_quality_gate_blocks_security_when_typecheck_fails()`
- `test_state_machine_transitions_from_code_green_to_quality_gate()`
- `test_state_machine_cannot_skip_quality_gate_to_security()`

### 8.2 Parsing
- `test_parse_cli_output_strips_transport_noise_from_raw_output()`
- `test_parse_cli_output_extracts_python_code_block()`
- `test_parse_cli_output_raises_when_output_exceeds_max_size()`
- `test_parse_cli_output_strips_ansi_sequences_from_clean_output()`

### 8.3 SPEC
- `test_spec_validator_raises_when_yaml_header_is_missing()`
- `test_spec_validator_passes_for_valid_spec_with_all_required_fields()`
- `test_spec_validator_raises_when_acceptance_criteria_is_empty()`
- `test_spec_validator_raises_when_objetivo_section_is_missing()`
- `test_spec_validator_raises_when_sections_use_h2_instead_of_h1()`

### 8.4 State machine / pipeline
- `test_state_machine_follows_minimal_happy_path_to_complete()`
- `test_state_machine_raises_on_invalid_transition()`
- `test_state_machine_includes_quality_gate_between_code_green_and_review()`
- `test_pipeline_engine_blocks_plan_when_spec_is_invalid()`
- `test_pipeline_engine_stops_at_plan_when_stop_at_is_plan()`
- `test_pipeline_engine_raises_when_executor_is_missing_for_required_step()`

### 8.5 Adapters
- `test_cli_execution_result_marks_timed_out_when_timeout_occurs()`
- `test_cli_execution_result_marks_failure_when_return_code_is_nonzero()`
- `test_cli_execution_result_rejects_invalid_return_code_type()`
- `test_all_adapters_return_cli_execution_result_with_valid_contract()`

### 8.6 Supervisor
- `test_supervisor_requests_retry_after_recoverable_step_failure()`
- `test_supervisor_reroutes_after_repeated_step_failures()`
- `test_supervisor_marks_terminal_failure_after_spec_validation_error()`
- `test_supervisor_returns_to_code_green_after_review_rejection()`

### 8.7 Worker
- `test_worker_picks_pending_run_and_transitions_to_running()`
- `test_worker_does_not_acquire_lock_for_already_locked_run()`
- `test_worker_requeues_step_after_retryable_failure()`
- `test_worker_generates_run_report_after_pipeline_completion()`
- `test_worker_does_not_process_run_already_in_completed_state()`

### 8.8 Persistência e relatório
- `test_run_repository_persists_run_state_after_execution()`
- `test_artifact_store_saves_raw_and_clean_outputs_by_step()`
- `test_run_report_contains_all_steps_tools_and_failures()`

---

## 9. Fixtures Recomendadas

> Legenda: ✅ = existente no repositório | 🔜 = aspiracional / a criar

```text
tests/
  fixtures/
    docker/
      valid_compose_config.txt          🔜
      invalid_compose_config.txt        🔜
    cli_outputs/
      multiple_python_blocks.txt        ✅
      noisy_no_code_block.txt           ✅
      gemini_plan.txt                   🔜
      codex_tests.txt                   🔜
      opencode_code.txt                 🔜
      claude_review.txt                 🔜
      noisy_mixed_output.txt            🔜
    specs/
      valid_feature_spec.md             ✅  (valid_spec.md)
      invalid_missing_yaml_spec.md      ✅
      invalid_missing_objetivo_spec.md  ✅
      invalid_empty_inputs_spec.md      ✅
      invalid_missing_id_spec.md        ✅
      invalid_h2_sections_spec.md       ✅
      invalid_acceptance_criteria.md    ✅
    reports/
      expected_run_report.md            🔜
```

---

## 10. Estrutura de Testes

> Legenda: ✅ = existe | 🔜 = aspiracional / a criar

```text
tests/
  unit/                                        ✅
    test_spec_validator.py                     ✅
    test_state_machine.py                      ✅
    test_parsing_engine.py                     ✅  (equivale a test_parsing_cleaners)
    test_contracts.py                          ✅
    test_config.py                             ✅
    test_cli_adapter.py                        ✅
    test_runtime_state.py                      ✅
    test_runtime_service_security.py           ✅
    test_persistence.py                        ✅
    test_pipeline_engine.py                    ✅
    test_repo_automation.py                    ✅
    test_docker_preflight.py                   🔜
    test_retry_policy.py                       🔜
    test_report_generator.py                   🔜
    test_security_gate.py                      🔜
  integration/                                 ✅
    test_cli_bootstrap.py                      ✅
    test_runtime_cli.py                        ✅
    test_pipeline_persistence.py               ✅
    test_adapter_parser_flow.py                🔜
    test_pipeline_memory_flow.py               🔜
  pipeline/                                    ✅
    test_happy_path.py                         ✅
    test_failure_recovery.py                   🔜
    test_review_rework.py                      🔜
  worker/                                      🔜
    test_worker_runtime.py                     🔜
    test_worker_locking.py                     🔜
  fixtures/                                    ✅
    specs/                                     ✅
    cli_outputs/                               ✅
```

### Sobre CLI simulation tests (nível 5.3)

Testes de simulação de subprocessos CLI **vivem em `tests/unit/`** enquanto o volume for pequeno. Quando o número de fixtures de output por ferramenta justificar, podem ser movidos para `tests/cli_simulation/`. Por enquanto, não há diretório separado — usar `tests/unit/test_cli_adapter.py` e arquivos de fixture em `tests/fixtures/cli_outputs/`.

### Configuração de testes assíncronos

Adapters e integrações assíncronas usam `pytest-asyncio`. A configuração `asyncio_mode = "auto"` está declarada em `pyproject.toml` em `[tool.pytest.ini_options]`. Todos os testes `async def` são coletados automaticamente sem decorator adicional.

---

## 11. Critérios de Qualidade
A suíte deve garantir:
- hand-offs confiáveis,
- validação rígida da SPEC,
- previsibilidade do AIgnt-Synapse-Flow,
- worker seguro para retries longos,
- `DOCKER_PREFLIGHT` executável e verificável,
- `SECURITY_REVIEW` funcionando como gate,
- relatórios de execução reproduzíveis,
- confiança para refatoração contínua.

## 12. Critérios de Saída do MVP
O MVP só deve ser considerado tecnicamente pronto quando houver testes cobrindo:
- bloqueio da feature quando `DOCKER_PREFLIGHT` falhar,
- SPEC inválida bloqueando a esteira,
- timeout de ferramenta,
- reroute básico,
- retorno de `REVIEW` para `CODE_GREEN`,
- gate de segurança antes de `REPORT`/`COMMIT`,
- run longa em worker,
- geração de `RUN_REPORT.md`,
- persistência de run, steps, eventos e artefatos em SQLite + filesystem (F07 ✅),
- lock inicial impedindo dupla aquisição da mesma run (F07 ✅).

## 13. Requisito de Testes de Integração por Feature

Testes de integração **são obrigatórios** para features que envolvam qualquer um dos seguintes:

| Categoria | Exemplos de feature |
|---|---|
| Lifecycle de runtime | start/stop/status do processo residente via CLI |
| Persistência | SQLite, filesystem de artefatos |
| Entrypoint público | comandos CLI que orquestram módulos reais |
| Adapter com subprocesso | execução de ferramenta externa real |
| Pipeline com módulos reais | pipeline engine + validator real (sem mocks totais) |

**Regra**: o `acceptance_criteria` de uma feature nessas categorias deve incluir ao menos um critério verificável **somente via teste de integração**. Critérios como "o CLI retorna sucesso ao executar X" ou "a run é registrada no banco após execução" são exemplos válidos.

Testes puramente unitários não substituem testes de integração quando o comportamento envolve I/O real ou encadeamento entre módulos distintos.
