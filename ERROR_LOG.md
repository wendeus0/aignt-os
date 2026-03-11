# ERROR_LOG

## 2026-03-11 - `repo-checks` da PR `#28` falhou por drift entre teste e API publica da pipeline

- Contexto: tentativa de preparar o merge da `F06-pipeline-engine-linear`.
- Ação/comando relacionado: `gh pr checks 28`, `gh run view 22966152999 --job 66670192469 --log-failed` e reproducao local com `PYTHONPATH=src ... python -m pytest tests/unit/test_pipeline_engine.py -k invalid -q`.
- Erro observado: o CI falhou em `tests/unit/test_pipeline_engine.py::test_pipeline_engine_blocks_plan_when_spec_is_invalid` com `AttributeError: module 'aignt_os.pipeline' has no attribute 'SpecValidationError'`.
- Causa identificada: o teste da `F06` ja modelava `SpecValidationError` como parte da API publica de `aignt_os.pipeline`, mas o modulo nao reexportava esse simbolo vindo de `aignt_os.specs`.
- Ação tomada: o modulo `src/aignt_os/pipeline.py` passou a reexportar `SpecValidationError`; a revalidacao local com `pytest`, `ruff`, `mypy` e `./scripts/commit-check.sh --sync-dev --skip-branch-validation --skip-docker --skip-security` voltou a fechar verde.
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
- Erro observado: `ModuleNotFoundError: No module named 'aignt_os'` em testes de config, contracts e CLI.
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
- Ação tomada: a pendência ficou aberta inicialmente; em 2026-03-10 o repositório foi revalidado com `env UV_CACHE_DIR=/home/g0dsssp33d/work/projects/aignt-os/.cache/uv uv run --no-sync ruff format --check .` e o gate voltou a fechar verde no estado atual.
- Status: resolvido no estado atual do repositório.
- Observação futura: revalidar após mudanças amplas de documentação ou baseline para garantir que `ruff format --check .` continue apto a operar como gate completo.

## 2026-03-09 08:40 - `.venv` local estava quebrada para executar `pytest`

- Contexto: tentativa de validar a feature de runtime persistente após integrar a branch no merge operacional.
- Ação/comando relacionado: `PYTHONPATH=src ./.venv/bin/pytest tests/integration/test_runtime_cli.py tests/unit/test_runtime_service_security.py tests/unit/test_runtime_state.py`
- Erro observado: `bad interpreter` apontando para `/home/g0dsssp33d/work/projetcs/aignt-os/.venv/bin/python3`.
- Causa identificada: virtualenv preexistente criada com caminho antigo/incorreto.
- Ação tomada: a validação migrou para um ambiente local novo dedicado (`.venv-codex-runtime`).
- Status: contornado na sessão.
- Observação futura: recriar ou remover a `.venv` antiga para evitar falso negativo em validações locais.

## 2026-03-09 08:42 - `uv run pytest` não enxergou dependências de runtime após `uv sync`

- Contexto: validação da suíte específica do runtime persistente depois de sincronizar dependências dev.
- Ação/comando relacionado: `env UV_CACHE_DIR=/home/g0dsssp33d/work/projects/aignt-os/.cache/uv uv run pytest tests/integration/test_runtime_cli.py tests/unit/test_runtime_service_security.py tests/unit/test_runtime_state.py`
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
- Causa identificada: wrappers de `.venv/bin/mypy` e `.venv/bin/pytest` apontavam para caminho antigo/incorreto em `/home/g0dsssp33d/work/projetcs/aignt-os/.venv/bin/python3`.
- Ação tomada: o fluxo operacional em `scripts/commit-check.sh` passou a executar `python -m mypy` e `python -m pytest` via `uv`; os testes operacionais do script foram ajustados para refletir o novo contrato.
- Status: resolvido.
- Observação futura: manter o fluxo com `python -m ...` reduz dependência de wrappers quebrados da `.venv`, mas a virtualenv local antiga ainda pode merecer limpeza dedicada fora desta frente.

## 2026-03-10 - PR `#19` falhou no `repo-checks` da F02

- Contexto: tentativa de fechar a feature `F02-spec-engine-mvp` com PR já aberta no GitHub.
- Ação/comando relacionado: `gh pr checks 19`, inspeção dos logs do GitHub Actions e revalidação local com `ruff`, `mypy`, `pytest` e `./scripts/commit-check.sh --sync-dev --skip-branch-validation --skip-docker --skip-security --allow-main`.
- Erro observado: `repo-checks` falhou por formatação pendente em `src/aignt_os/specs/validator.py`, import order em `tests/unit/test_spec_validator.py` e `mypy` reclamando de `Library stubs not installed for "yaml"`.
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
