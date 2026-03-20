# ERROR_LOG

## 2026-03-20 - PR `#98` abriu com `repo-checks` falhando por baseline de formatacao fora do delta funcional

- Contexto: fechamento Git da onda `F51-runtime-boundaries-foundation` -> `F53-observability-runtime-events` e abertura da PR `#98`.
- Ação/comando relacionado: `gh pr checks 98`, `gh run view 23332947262 --log-failed`, `./scripts/commit-check.sh --no-sync --skip-branch-validation --skip-docker --skip-security --allow-main`.
- Erro observado: o job `repo-checks` falhou em `ruff format --check .` por tres arquivos fora do baseline esperado (`src/synapse_os/state_machine.py`, `tests/integration/test_gemini_adapter.py`, `tests/integration/test_spec_validation_gate.py`), embora o delta funcional de `F51` -> `F53` estivesse validado.
- Causa identificada: resíduo de higiene de repositório fora do recorte funcional da frente, detectado apenas no gate amplo do CI.
- Ação tomada: a branch da PR recebeu um commit operacional mínimo (`ci(repo): fix repo-checks formatting baseline`) com normalização de formatação e remoção de import não usado; a PR `#98` foi então revalidada e mergeada.
- Status: resolvido e absorvido em `origin/main`.
- Observação futura: antes de concluir o fluxo Git de frentes grandes, rodar o equivalente local do `repo-checks` no modo amplo para evitar que a PR abra verde no recorte funcional, mas vermelha por hygiene global da baseline.

## 2026-03-13 - PR `#87` da F40 entrou com delta misto alem do recorte funcional

- Contexto: reavaliacao do baseline apos a merge da `F40-local-cancellation`.
- Ação/comando relacionado: `gh pr view 87 --json title,body,files`, inspecao de `origin/main` e checagem do handoff duravel.
- Erro observado: a PR `#87` mergeou `F40`, mas o diff remoto incluiu tambem mudancas documentais/operacionais fora do recorte funcional estrito da feature, e `features/F40-local-cancellation/` ficou sem `NOTES.md`, `CHECKLIST.md` e `REPORT.md`.
- Causa identificada: fechamento Git da feature sem uma passada posterior de consolidacao do baseline e do handoff, mantendo a linha principal funcionalmente correta mas documentalmente desalinhada.
- Ação tomada: abrir a chore doc-only `chore-post-f40-f42-baseline-sync` para registrar o incidente, retrocompletar os artefatos minimos de `F40`/`F42` e alinhar `memory.md`, `PENDING_LOG.md`, `README.md` e `CHANGELOG.md` ao estado real de `main`.
- Status: mitigado pela chore de sync/handoff; nao houve reabertura de escopo funcional nem reversao da merge.
- Observação futura: quando uma PR funcional entrar com delta misto inevitavel, consolidar imediatamente o handoff duravel e os artefatos minimos da feature em vez de deixar o baseline documental em estado parcial.

## 2026-03-13 - Branch `feature/f39-persistence-path-root-hardening` acumulou drafts pos-MVP fora de escopo

- Contexto: triagem tecnica e limpeza operacional apos `F39` e `F37` ja estarem absorvidas em `origin/main`.
- Ação/comando relacionado: `git log --oneline origin/main..HEAD`, `./scripts/branch-sync-check.sh`, extracao controlada para `archive/*` e `draft/*`.
- Erro observado: a branch local nomeada como `F39` estava `ahead=1 behind=1` contra `origin/main`, carregando um commit de `F47` e mudancas locais misturadas de `F41`, `F43`, `F44`, `F45`, `F46` e `F42`.
- Causa identificada: reuso de uma branch ja absorvida no baseline para rascunhos de multiplas frentes futuras, quebrando a regra de uma feature por vez e inviabilizando `branch-sync-update`.
- Ação tomada: o estado misto foi preservado em `origin/archive/2026-03-13-f39-drift-snapshot`; os recortes determinísticos foram separados e publicados como `origin/draft/f41-dashboard-artifacts-explorer`, `origin/draft/f43-runtime-robustness`, `origin/draft/f44-auth-backend-abstraction`, `origin/draft/f45-tui-performance-optimization` e `origin/draft/f47-advanced-rbac`; o restante transversal ficou apenas no archive branch.
- Status: resolvido operacionalmente; a linha ativa voltou a partir de `origin/main`.
- Observação futura: nunca reutilizar branch de feature ja mergeada para drafts novos; estacionar exploracoes futuras em `draft/*` ou `archive/*` e rodar `technical-triage` em branch limpa antes de abrir nova frente.

## 2026-03-13 - PR `#65` da F30 mergeada com `repo-checks` falhando por formatacao global, depois resolvido pela `#66`

- Contexto: fechamento Git da `F30-auth-registry-cli` apos quality gate local e abertura da PR `#65`.
- Ação/comando relacionado: `gh pr checks 65`, `gh run view 23034742953 --job 66900277313 --log-failed` e revalidacao local com `env UV_CACHE_DIR=/home/g0dsssp33d/work/projects/synapse-os/.cache/uv uv run --no-sync ruff format --check .`.
- Erro observado: o job `repo-checks` da PR falhou porque `ruff format --check .` ainda listava 6 arquivos fora do padrao (`src/synapse_os/persistence.py`, `tests/integration/test_runs_cli.py`, `tests/unit/test_cli_adapter.py`, `tests/unit/test_parsing_engine.py`, `tests/unit/test_persistence.py`, `tests/unit/test_security.py`).
- Causa identificada: divida de formatacao preexistente na baseline atual, fora do diff funcional da `F30`.
- Ação tomada: a PR foi mergeada com aprovacao explicita por excecao; a correcao do gate virou a proxima frente prioritaria de estabilizacao da baseline.
- Status: resolvido; a baseline foi restaurada na PR `#66` e o handoff pos-`F32` nao deve mais tratar este incidente como bloqueio aberto.
- Observação futura: manter a checagem local equivalente do `repo-checks` antes de concluir PRs novas, para evitar depender de merge administrativo por debt global fora do diff.

## 2026-03-12 - Regressao de compatibilidade no monkeypatch de `_dispatch_service` durante a F29

- Contexto: implementacao e validacao final da `F29-auth-rbac-foundation`.
- Ação/comando relacionado: `env UV_CACHE_DIR=/home/g0dsssp33d/work/projects/synapse-os/.cache/uv uv run --no-sync python -m pytest tests/unit/test_config.py tests/unit/test_auth.py tests/integration/test_cli_auth_rbac.py tests/integration/test_runs_submit_cli.py tests/integration/test_runtime_cli.py tests/integration/test_cli_error_model.py -q`
- Erro observado: `tests/integration/test_cli_error_model.py::test_runs_submit_unexpected_dispatch_failure_returns_execution_error_code` falhou com `TypeError` porque o monkeypatch local de `_dispatch_service` nao aceitava o novo keyword argument `initiated_by`.
- Causa identificada: a F29 ampliou `_dispatch_service()` para aceitar override de provenance autenticada, mas o call site de `runs submit` perdeu compatibilidade com o patch zero-arg exercitado pelos testes legados da F21.
- Ação tomada: o call site foi ajustado para chamar `_dispatch_service()` sem argumentos quando nao houver principal autenticado e usar o override apenas no caminho autenticado.
- Status: resolvido localmente e mergeado em `main` via PR `#63`.
- Observação futura: ao ampliar helpers de CLI ja usados por monkeypatch em testes de integracao, preservar assinatura compatível ou atualizar explicitamente os doubles legados no mesmo delta.

## 2026-03-11 19:26 -03 - Smoke real do Codex falhou por autenticacao ausente

- Contexto: validacao operacional da `F12-codex-adapter-operational-hardening` apos `DOCKER_PREFLIGHT` completo e hardening do `CodexCLIAdapter`.
- Ação/comando relacionado: `./scripts/dev-codex.sh -- exec --color never "Reply with OK only."`
- Erro observado: `401 Unauthorized: Missing bearer or basic authentication in header` retornado pelo Codex apos o launcher/container-first iniciar corretamente.
- Causa identificada: credencial de autenticacao ausente ou invalida para o provider do Codex no ambiente real; nao houve falha do adapter nem do launcher Docker.
- Ação tomada: o caso foi classificado na F12 como `authentication_unavailable`, tratado como bloqueio operacional explicito e nao como falha funcional do `CodexCLIAdapter`.
- Status: conhecido e nao bloqueante para o merge da F12.
- Observação futura: revalidar o smoke autenticado apenas quando houver necessidade real de uso do Codex com credencial valida; nao abrir subsistema de autenticacao dedicado sem demanda concreta.

## 2026-03-11 17:44 -03 - Worktree fria da F09 sem dependencias dev para coleta de testes

- Contexto: implementacao da `F09-supervisor-mvp` em worktree nova.
- Ação/comando relacionado: `pytest tests/unit/test_supervisor.py ... tests/integration/test_pipeline_persistence.py` e `env UV_CACHE_DIR=/home/g0dsssp33d/work/projects/synapse-os/.cache/uv uv run pytest ...`
- Erro observado: `ModuleNotFoundError: No module named 'typer'` durante a carga de `tests/integration/conftest.py`.
- Causa identificada: a worktree foi aberta sem bootstrap de dependencias dev; a coleta dos testes de integracao depende de `typer`.
- Ação tomada: `env UV_CACHE_DIR=/home/g0dsssp33d/work/projects/synapse-os/.cache/uv uv sync --locked --extra dev` e reexecucao da suite no ambiente sincronizado.
- Status: resolvido localmente.
- Observação futura: em worktree fria, sincronizar extras de desenvolvimento antes de rodar suites que carregam `tests/integration/conftest.py`.

## 2026-03-11 17:44 -03 - `mypy src tests` continua falhando por modulo duplicado `conftest`

- Contexto: validacao final da `F09-supervisor-mvp` antes do handoff.
- Ação/comando relacionado: `env UV_CACHE_DIR=/home/g0dsssp33d/work/projects/synapse-os/.cache/uv uv run mypy src tests`
- Erro observado: `tests/unit/conftest.py: error: Duplicate module named "conftest" (also at "tests/integration/conftest.py")`.
- Causa identificada: a invocacao ampla `mypy src tests` conflitou primeiro com os dois `conftest.py` como modulos top-level e, apos resolver o namespace, expôs que a arvore `tests/` nao seguia o mesmo contrato strict aplicado a `src/synapse_os`.
- Ação tomada: na branch `chore/test-layout-typecheck-hardening`, a arvore `tests/` recebeu package markers (`tests/`, `tests/unit/`, `tests/integration/`, `tests/pipeline/`) e o `pyproject.toml` passou a declarar override explícito de `mypy` para `tests` e `tests.*`. A revalidação com `uv run mypy src tests`, `uv run --no-sync python -m mypy`, `pytest` e `./scripts/commit-check.sh --sync-dev --skip-docker` fechou verde.
- Status: resolvido.
- Observação futura: manter o contrato strict de `mypy` centrado em `src/synapse_os`; tipagem estrita da arvore `tests/` só deve virar frente própria se houver benefício real.

## 2026-03-11 - `test_adapter_parser_flow` falhou por fixture ANSI como texto literal

- Contexto: criação dos testes de integração do parsing engine na branch `chore/tdd-integration-hardening`.
- Ação/comando relacionado: `uv run --no-sync python -m pytest tests/integration/test_adapter_parser_flow.py`
- Erro observado: `assert '\x1b[' in result.stdout_raw` falhou porque `noisy_mixed_output.txt` armazena sequências ANSI como text literals `\u001b[32m` (6 chars), não como o byte ESC real (`\x1b`, chr(27)).
- Causa identificada: `_read_fixture()` sem `unicode_escape=True` retorna os chars literais `\u001b`, que o parser não reconhece como sequências ANSI. O padrão correto já existia nos testes unitários mas não foi replicado na versão de integração.
- Ação tomada: `_read_fixture()` em `test_adapter_parser_flow.py` passou a aceitar `unicode_escape=True`; todos os usos de `noisy_mixed_output.txt` foram atualizados.
- Status: resolvido.
- Observação futura: fixtures com ANSI armazenado como escape literal requerem `unicode_escape=True` no helper de leitura. Considerar documentar isso em comentário nos arquivos `noisy_mixed_output.txt` e `noisy_no_code_block.txt`.

## 2026-03-11 - Assertiva incorreta sobre `[rpc]` no teste de parsing

- Contexto: expansão do `test_parsing_engine.py` durante hardening TDD.
- Ação/comando relacionado: `uv run --no-sync python -m pytest tests/unit/test_parsing_engine.py`
- Erro observado: `assert "[rpc]" not in parsed_output.stdout_clean` falhou; o parser remove apenas `[transport]` (via `TRANSPORT_NOISE_PREFIXES`), não `[rpc]`.
- Causa identificada: o teste assumiu que `[rpc]` seria tratado como ruído operacional, mas `parsing.py:16` define apenas `("[transport]",)` como prefixo a remover.
- Ação tomada: a assertiva incorreta foi removida. O comportamento do parser (não remover `[rpc]`) está correto por design.
- Status: resolvido.
- Observação futura: qualquer expansão de `TRANSPORT_NOISE_PREFIXES` para incluir `[rpc]` ou outros prefixos deve ser uma decisão explícita documentada, não uma suposição de teste.

## 2026-03-11 - `repo-checks` da PR `#28` falhou por drift entre teste e API publica da pipeline

- Contexto: tentativa de preparar o merge da `F06-pipeline-engine-linear`.
- Ação/comando relacionado: `gh pr checks 28`, `gh run view 22966152999 --job 66670192469 --log-failed` e reproducao local com `PYTHONPATH=src ... python -m pytest tests/unit/test_pipeline_engine.py -k invalid -q`.
- Erro observado: o CI falhou em `tests/unit/test_pipeline_engine.py::test_pipeline_engine_blocks_plan_when_spec_is_invalid` com `AttributeError: module 'synapse_os.pipeline' has no attribute 'SpecValidationError'`.
- Causa identificada: o teste da `F06` ja modelava `SpecValidationError` como parte da API publica de `synapse_os.pipeline`, mas o modulo nao reexportava esse simbolo vindo de `synapse_os.specs`.
- Ação tomada: o modulo `src/synapse_os/pipeline.py` passou a reexportar `SpecValidationError`; a revalidacao local com `pytest`, `ruff`, `mypy` e `./scripts/commit-check.sh --sync-dev --skip-branch-validation --skip-docker --skip-security` voltou a fechar verde.
- Status: resolvido localmente; PR pendente de atualizacao no GitHub.
- Observação futura: quando a feature introduzir novo modulo de orquestracao, manter teste e API publica alinhados explicitamente para evitar regressao em `repo-checks`.

## 2026-03-11 - Corpo de PR inline sofreu expansao de shell durante `gh pr create`

- Contexto: fechamento Git da branch `chore/docker-preflight-modes` com abertura de PR no sandbox.
- Ação/comando relacionado: `gh pr create --body "...markdown com backticks..."`.
- Erro observado: o shell expandiu trechos do corpo Markdown como substituição de comando, gerando mensagens como `zsh:1: command not found: DOCKER_PREFLIGHT` e publicando uma descrição de PR corrompida.
- Causa identificada: uso de `gh pr create --body` com texto inline contendo backticks e conteúdo shell-sensitive, sem encapsulamento seguro em arquivo.
- Ação tomada: a PR foi aberta, o corpo publicado foi inspecionado e corrigido imediatamente com `gh pr edit --body-file /tmp/pr24-body.md`.
- Status: resolvido.
- Observação futura: no fluxo Git assistido por agente, preferir `gh pr create --body-file` ou `gh pr edit --body-file` por padrão para evitar expansão acidental de shell em descrições Markdown.

## 2026-03-11 - `dev-codex.sh` caiu em symlink legada no volume `codex-home`

- Contexto: validacao do startup minimo do Codex apos endurecer o baseline MCP no `codex-dev`.
- Acao/comando relacionado: `./scripts/dev-codex.sh -- --version`
- Erro observado: `cp: '/workspace/.codex/config.toml' and '/home/codex/.codex/config.toml' are the same file`.
- Causa identificada: o volume persistido `codex-home` ainda guardava uma symlink legada de `config.toml`, criada antes da troca de estrategia de geracao da configuracao efetiva.
- Acao tomada: o launcher foi endurecido e a renderizacao da config efetiva foi extraida para `scripts/render-codex-config.sh`, eliminando dependencia da symlink antiga.
- Status: resolvido.
- Observacao futura: manter o launcher responsavel por gerar a config efetiva no volume do `codex-dev`, sem depender de symlink persistida entre execucoes.

## 2026-03-09 06:00 - Falha de `uv run` por cache fora da workspace

- Contexto: validação operacional local durante revisão e correção de workflows/scripts.
- Ação/comando relacionado: `uv run pytest tests/unit/test_repo_automation.py`
- Erro observado: falha ao inicializar cache em `/home/g0dsssp33d/.cache/uv` com `Permission denied`.
- Causa identificada: ambiente sandbox bloqueando escrita no cache padrão do `uv` fora da workspace.
- Ação tomada: validação local migrou para `.venv` existente e, quando possível, para `UV_CACHE_DIR` dentro da workspace.
- Status: contornado na sessão.
- Observação futura: validar fora do sandbox se o fluxo padrão de `uv run` está consistente no ambiente do operador.

## 2026-03-09 06:02 - Falha de rede ao sincronizar dependências com `uv`

- Contexto: tentativa de executar `commit-check` e sincronizar dependências pelo caminho operacional padrão.
- Ação/comando relacionado: `uv sync --locked --extra dev`, `uv run ...`, `./scripts/commit-check.sh --skip-branch-validation --skip-docker`
- Erro observado: falha para baixar `pyyaml==6.0.3` por `dns error` e `Temporary failure in name resolution`.
- Causa identificada: ambiente sem acesso de rede para resolver/baixar dependências.
- Ação tomada: reexecução fora do sandbox quando necessário; validações locais alternativas usaram `.venv` já presente e testes com `PYTHONPATH=src`.
- Status: contornado na sessão; não validado pelo caminho de rede real.
- Observação futura: revalidar `uv sync --locked --extra dev` em ambiente com rede antes de concluir o ciclo operacional completo.

## 2026-03-09 06:04 - `commit-check` sem dependências dev preparadas

- Contexto: validação operacional local em ambiente limpo.
- Ação/comando relacionado: `./scripts/commit-check.sh --skip-branch-validation --skip-docker`
- Erro observado: `error: Failed to spawn: ruff`.
- Causa identificada: o script assumia ferramentas dev instaladas sem sincronização prévia.
- Ação tomada: ajuste operacional posterior para tornar o bootstrap explícito com `--sync-dev`, mantendo `uv run --no-sync` no fluxo padrão.
- Status: resolvido.
- Observação futura: documentar o uso de `--sync-dev` para bootstrap local.

## 2026-03-09 06:08 - `pytest` da `.venv` sem `PYTHONPATH=src`

- Contexto: execução local de testes após corrigir baseline operacional.
- Ação/comando relacionado: `./.venv/bin/pytest`
- Erro observado: `ModuleNotFoundError: No module named 'synapse_os'` em testes de config, contracts e CLI.
- Causa identificada: execução local usando `.venv` sem instalar o pacote ou sem `PYTHONPATH=src`; o caminho operacional do CI continua sendo `uv run pytest`.
- Ação tomada: validação local da suíte foi feita com `PYTHONPATH=src ./.venv/bin/pytest`.
- Status: contornado na sessão.
- Observação futura: validar se vale padronizar explicitamente o import path local fora do fluxo `uv run`.

## 2026-03-09 - Docker preflight bloqueado no sandbox

- Contexto: validação do `DOCKER_PREFLIGHT` da worktree antes de iniciar a feature.
- Ação/comando relacionado: `./scripts/docker-preflight.sh`
- Erro observado: build falhou com `Docker daemon is not accessible`.
- Causa identificada: limitação de acesso ao daemon Docker no sandbox, não erro do repositório.
- Ação tomada: reexecução fora do sandbox; `compose config` e build passaram.
- Status: resolvido.
- Observação futura: manter diferenciação explícita entre falha de sandbox e falha real do preflight.

## 2026-03-09 - Check local bloqueado por DNS no sandbox

- Contexto: execução inicial de checks operacionais locais.
- Ação/comando relacionado: `./scripts/commit-check.sh --skip-branch-validation --skip-docker`
- Erro observado: `uv` falhou ao baixar dependências com erro de DNS/resolução.
- Causa identificada: restrição de rede no sandbox.
- Ação tomada: reexecução fora do sandbox.
- Status: resolvido.
- Observação futura: manter cache local e usar elevação apenas quando necessário para distinguir ambiente de repositório.

## 2026-03-09 - Runtime stop aceitava risco de sinalizar PID arbitrário

- Contexto: implementação inicial do runtime persistente mínimo.
- Ação/comando relacionado: testes de segurança do runtime (`pytest tests/integration/test_runtime_cli.py tests/unit/test_runtime_state.py tests/unit/test_runtime_service_security.py`)
- Erro observado: `stop` confiava em PID persistido e não validava identidade adicional do processo.
- Causa identificada: hardening local ausente na primeira implementação do lifecycle.
- Ação tomada: adição de `process_identity`, validação via `/proc/<pid>/cmdline`, falha segura em mismatch, escrita atômica e permissões restritas no arquivo de estado.
- Status: resolvido.
- Observação futura: a validação continua Linux-first e o endurecimento de path ainda é básico no MVP.

## 2026-03-09 - Formatação do repositório fora do escopo da feature

- Contexto: execução do fluxo operacional completo.
- Ação/comando relacionado: `UV_CACHE_DIR=.cache/uv uv run ruff format --check .`
- Erro observado: arquivos preexistentes fora do padrão de formatação.
- Causa identificada: dívida de formatação já presente no repositório, não ligada ao runtime persistente.
- Ação tomada: a pendência ficou aberta inicialmente; em 2026-03-10 o repositório foi revalidado com `env UV_CACHE_DIR=/home/g0dsssp33d/work/projects/synapse-os/.cache/uv uv run --no-sync ruff format --check .` e o gate voltou a fechar verde no estado atual.
- Status: resolvido no estado atual do repositório.
- Observação futura: revalidar após mudanças amplas de documentação ou baseline para garantir que `ruff format --check .` continue apto a operar como gate completo.

## 2026-03-09 08:40 - `.venv` local estava quebrada para executar `pytest`

- Contexto: tentativa de validar a feature de runtime persistente após integrar a branch no merge operacional.
- Ação/comando relacionado: `PYTHONPATH=src ./.venv/bin/pytest tests/integration/test_runtime_cli.py tests/unit/test_runtime_service_security.py tests/unit/test_runtime_state.py`
- Erro observado: `bad interpreter` apontando para `/home/g0dsssp33d/work/projetcs/synapse-os/.venv/bin/python3`.
- Causa identificada: virtualenv preexistente criada com caminho antigo/incorreto.
- Ação tomada: a validação migrou para um ambiente local novo dedicado (`.venv-codex-runtime`).
- Status: contornado na sessão.
- Observação futura: recriar ou remover a `.venv` antiga para evitar falso negativo em validações locais.

## 2026-03-09 08:42 - `uv run pytest` não enxergou dependências de runtime após `uv sync`

- Contexto: validação da suíte específica do runtime persistente depois de sincronizar dependências dev.
- Ação/comando relacionado: `env UV_CACHE_DIR=/home/g0dsssp33d/work/projects/synapse-os/.cache/uv uv run pytest tests/integration/test_runtime_cli.py tests/unit/test_runtime_service_security.py tests/unit/test_runtime_state.py`
- Erro observado: `ModuleNotFoundError: No module named 'typer'` durante a coleta.
- Causa identificada: o runner usado pelo `uv run` permaneceu desalinhado com o ambiente esperado para a sessão.
- Ação tomada: instalação do projeto e extras de desenvolvimento em uma virtualenv local dedicada (`.venv-codex-runtime`) e reexecução da suíte por esse ambiente.
- Status: contornado na sessão.
- Observação futura: validar se o fluxo preferido do projeto para testes locais deve ser `uv run` ou uma virtualenv explícita quando houver sandbox/ambiente misto.

## 2026-03-09 - Conflito transitório de nome de container no `codex-dev`

- Contexto: validação operacional da infraestrutura isolada de desenvolvimento do Codex na branch `chore/devcontainer-codex-isolation`.
- Ação/comando relacionado: `docker compose -f compose.yaml -f compose.dev.yaml up -d codex-dev`, `./scripts/dev-codex.sh -- --version`
- Erro observado: conflito de nome de container ao executar o launcher enquanto um `compose up` manual concorrente recriava `codex-dev`.
- Causa identificada: corrida operacional entre subida manual do serviço e execução do launcher, não falha estrutural do `compose.dev.yaml`.
- Ação tomada: validação refeita em série, com `codex-dev` já estável antes do launcher.
- Status: resolvido.
- Observação futura: usar `./scripts/dev-codex.sh` como entrypoint principal do ambiente para evitar corrida de recriação do container.

## 2026-03-09 - Branch Sync Gate bloqueou finalização com drift e worktree suja

- Contexto: tentativa de fechamento da branch antes do push/PR da frente operacional.
- Ação/comando relacionado: `./scripts/branch-sync-check.sh`
- Erro observado: a checagem reportou `behind=1`, bloqueando a finalização até a branch voltar a um estado sincronizável.
- Causa identificada: drift temporário com `origin/main` combinado com worktree ainda suja, impedindo atualização segura pela Branch Sync Gate.
- Ação tomada: o bloqueio foi respeitado; a finalização só ficou liberada após a branch voltar a um estado limpo e à frente do remoto da própria branch.
- Status: resolvido.
- Observação futura: rodar `./scripts/branch-sync-check.sh` cedo e manter a worktree limpa antes de tentar `commit`/`push`/`PR`.

## 2026-03-10 - `uv run --no-sync` caiu em wrappers quebrados da `.venv`

- Contexto: revalidação operacional do fluxo local após `uv sync --locked --extra dev` em ambiente com rede liberada.
- Ação/comando relacionado: `./scripts/commit-check.sh --no-sync --skip-branch-validation --skip-docker --skip-security`, `uv run --no-sync mypy`, `uv run --no-sync pytest`
- Erro observado: `uv run --no-sync mypy` falhou com `No such file or directory`; o mesmo padrão afetava wrappers da `.venv` usados no passo de testes.
- Causa identificada: wrappers de `.venv/bin/mypy` e `.venv/bin/pytest` apontavam para caminho antigo/incorreto em `/home/g0dsssp33d/work/projetcs/synapse-os/.venv/bin/python3`.
- Ação tomada: o fluxo operacional em `scripts/commit-check.sh` passou a executar `python -m mypy` e `python -m pytest` via `uv`; os testes operacionais do script foram ajustados para refletir o novo contrato.
- Status: resolvido.
- Observação futura: manter o fluxo com `python -m ...` reduz dependência de wrappers quebrados da `.venv`, mas a virtualenv local antiga ainda pode merecer limpeza dedicada fora desta frente.

## 2026-03-10 - PR `#19` falhou no `repo-checks` da F02

- Contexto: tentativa de fechar a feature `F02-spec-engine-mvp` com PR já aberta no GitHub.
- Ação/comando relacionado: `gh pr checks 19`, inspeção dos logs do GitHub Actions e revalidação local com `ruff`, `mypy`, `pytest` e `./scripts/commit-check.sh --sync-dev --skip-branch-validation --skip-docker --skip-security --allow-main`.
- Erro observado: `repo-checks` falhou por formatação pendente em `src/synapse_os/specs/validator.py`, import order em `tests/unit/test_spec_validator.py` e `mypy` reclamando de `Library stubs not installed for "yaml"`.
- Causa identificada: o delta da F02 foi commitado sem alinhar completamente os gates locais de formatação, lint e tipagem exigidos pelo CI.
- Ação tomada: correção mínima no `SpecValidator` e no teste afetado, com revalidação local completa dos mesmos gates usados no CI.
- Status: resolvido na branch atual.
- Observação futura: manter a reexecução explícita do `repo-checks` local equivalente antes de concluir novas atualizações da PR.

## 2026-03-11 05:40 - Configuração do Codex aplicada inicialmente no alvo errado

- Contexto: ajuste operacional do ambiente local do Codex para multi-agent e fluxo de planejamento.
- Ação/comando relacionada: criação inicial de scaffolding paralelo fora de `.codex/config.toml` e validações com `./scripts/dev-codex.sh -- features list` e `./scripts/dev-codex.sh -- mcp list`.
- Erro observado: a mudança foi implementada inicialmente fora do alvo correto do Codex; durante a validação do launcher houve ainda uma falha transitória de configuração renderizada com `duplicate key` em `mcp_servers.github`.
- Causa identificada: interpretação incorreta do objetivo inicial e necessidade de validar o config efetivo renderizado do Codex no `codex-dev`.
- Ação tomada: remoção dos arquivos criados fora do alvo, correção em `.codex/config.toml` e `scripts/dev-codex.sh`, revalidação dos perfis `container_planning` e `container_aggressive`, da feature `multi_agent` e dos MCPs efetivos.
- Status: resolvido.
- Observação futura: confirmar primeiro se a mudança desejada é na configuração do Codex ou no scaffolding do projeto e sempre validar o config efetivo renderizado do launcher.
