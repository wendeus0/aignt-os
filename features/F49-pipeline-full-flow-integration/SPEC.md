---
id: F49-pipeline-full-flow-integration
type: feature
summary: Adicionar testes de integração do PipelineEngine cobrindo o fluxo completo CODE_GREEN → REVIEW → SECURITY → DOCUMENT → COMPLETE.
inputs:
  - PipelineEngine com executores fake injetados para todos os estados
  - SPEC.md válida de fixture
outputs:
  - step_history com todos os estados executados em ordem
  - context.current_state == "COMPLETE" ao final
  - artefatos de cada estado acessíveis em context.artifacts
acceptance_criteria:
  - Um teste de pipeline exercita o caminho completo CODE_GREEN → QUALITY_GATE → REVIEW → SECURITY → DOCUMENT → COMPLETE com executores fake para todos os estados e verifica que step_history contém todos eles em ordem.
  - Um teste verifica que stop_at="DOCUMENT" retorna context.current_state == "DOCUMENT" e que COMPLETE não foi atingido.
  - Um teste verifica que o artefato "run_report_md" produzido pelo executor fake do estado DOCUMENT está presente em context.artifacts.
  - Um teste migrado de test_review_rework.py exercita a transição REVIEW → CODE_GREEN (rework) pelo PipelineEngine injetando um supervisor que retorna return_to_code_green, verificando que context.step_history registra o desvio.
  - Um teste verifica que o caminho completo sem rework avança de TEST_RED até COMPLETE sem erro.
non_goals:
  - Implementar executores reais para REVIEW, SECURITY ou DOCUMENT (esses executores permanecem injetáveis).
  - Integrar reporting.py ao executor de DOCUMENT (escopo de feature futura).
  - Adicionar novo comportamento ao PipelineEngine ou ao Synapse-Flow.
  - Modificar stop_at nem PIPELINE_STOP_STATES.
  - Testar comportamento de runtime persistido (PersistedPipelineRunner) ou worker.
---

# Contexto

O `PipelineEngine` — parte central do Synapse-Flow, a engine própria de pipeline do SynapseOS — já despacha todos os estados do fluxo linear, incluindo `REVIEW`, `SECURITY` e `DOCUMENT`, via `_run_runtime_step()`. Porém:

1. `tests/pipeline/test_happy_path.py` cobre o pipeline até `SECURITY` com `stop_at` parametrizado, mas não testa o estado `DOCUMENT` nem o fluxo completo até `COMPLETE`.
2. `tests/pipeline/test_review_rework.py` foi escrito como documentação de comportamento futuro, exercitando a state machine diretamente. O arquivo registra explicitamente: *"quando o Supervisor/pipeline for implementado para esses estados, migrar para testes de integração"*. Esse momento chegou com o suporte de F48 ao gate de validação e a consolidação do PIPELINE_STEPS.
3. O caminho `DOCUMENT → COMPLETE` nunca foi exercitado em nenhum teste de pipeline existente.

Esse gap significa que o Synapse-Flow não tem cobertura de integração para o trecho final do seu fluxo oficial, tornando invisíveis regressões em qualquer mudança futura nos estados pós-SECURITY.

# Objetivo

Fechar o gap de cobertura do Synapse-Flow adicionando testes de integração do `PipelineEngine` que:

1. Exercitam o fluxo completo `CODE_GREEN → QUALITY_GATE → REVIEW → SECURITY → DOCUMENT → COMPLETE` com executores fake, verificando `step_history` e `context.current_state`.
2. Validam `stop_at="DOCUMENT"` como ponto de parada legítimo.
3. Migram o comportamento de rework documentado em `test_review_rework.py` para testes que usam `PipelineEngine` diretamente, com supervisor injetado retornando `return_to_code_green` no estado `REVIEW`.
4. Garantem que artefatos produzidos pelos executores de `DOCUMENT` ficam acessíveis em `context.artifacts`.

Nenhuma mudança de produção é necessária — a feature é exclusivamente de teste.

## Restrições técnicas

- Todos os novos testes ficam em `tests/pipeline/` para manter separação de níveis (`unit/` para contratos isolados, `pipeline/` para exercício do fluxo end-to-end com fakes).
- Os executores fake devem seguir o padrão já estabelecido em `test_happy_path.py` (`_FakeExecutor`).
- Para o teste de rework, usar `Supervisor` real com `max_retries=0` ou implementar supervisor stub que retorna `return_to_code_green` diretamente — sem mockar internos do PipelineEngine.
- `DOCKER_PREFLIGHT` não é necessário: nenhum subprocess real é invocado.
