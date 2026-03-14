# F20 Report

## Resumo executivo

- A F20 adiciona um onboarding publico curto para a primeira run diretamente no `README.md`.
- A mitigacao do risco residual da F19 entrou pelo eixo correto: clarificar expectativa do operador, sem ampliar `synapse doctor` nem substituir preflight operacional.
- O caminho oficial permaneceu local e `sync-first`, com troubleshooting essencial e boundary explicito para `repo-preflight`.

## Escopo alterado

- Materializacao da feature em `features/F20-public-onboarding/` com `SPEC.md`, `NOTES.md`, `CHECKLIST.md` e este `REPORT.md`.
- Novo quickstart publico curto e troubleshooting essencial em `README.md`.
- Teste documental de contrato e smoke de integracao da sequencia publica em `tests/unit/test_public_onboarding_docs.py` e `tests/integration/test_public_onboarding_flow.py`.

## Validacoes executadas

- `env UV_CACHE_DIR=/home/g0dsssp33d/work/projects/synapse-os/.cache/uv uv run --no-sync python -m pytest tests/unit/test_public_onboarding_docs.py tests/integration/test_public_onboarding_flow.py -q`
- `env UV_CACHE_DIR=/home/g0dsssp33d/work/projects/synapse-os/.cache/uv uv run --no-sync python -m pytest tests/unit/test_public_onboarding_docs.py tests/integration/test_public_onboarding_flow.py tests/integration/test_doctor_cli.py tests/integration/test_runs_submit_cli.py tests/integration/test_runs_cli.py -q`
- `env UV_CACHE_DIR=/home/g0dsssp33d/work/projects/synapse-os/.cache/uv uv run --no-sync ruff check tests/unit/test_public_onboarding_docs.py tests/integration/test_public_onboarding_flow.py`
- `env UV_CACHE_DIR=/home/g0dsssp33d/work/projects/synapse-os/.cache/uv uv run --no-sync python -m mypy tests/unit/test_public_onboarding_docs.py tests/integration/test_public_onboarding_flow.py`

## Security review

- Risco identificado: baixo. O delta nao adiciona shell, subprocesso novo, Docker, rede, leitura arbitraria nem mudanca no contrato de execucao da CLI.
- Mitigacao aplicada: o onboarding deixa explicito que `synapse doctor` e advisory/local e nao deve ser usado como bypass de `repo-preflight` para cenarios operacionais mais pesados.
- Parecer: aprovado com ressalvas baixas.

## Riscos residuais

- O quickstart continua intencionalmente curto; ele nao substitui documentacao operacional mais ampla se o projeto passar a exigir Docker, runtime persistente ou credenciais externas no fluxo minimo.
- A branch atual segue com drift estrutural em relacao a `origin/main` (`ahead=1 behind=1`) por causa do merge commit da F19 em `main`, embora `git diff HEAD..origin/main` esteja vazio; o gate de sync final ainda precisa ser respeitado antes de push/PR.

## Follow-ups

- Usar `git-flow-manager` para preparar o commit da F20 depois da rechecagem final de branch sync.
- Reavaliar em frente propria apenas se onboarding precisar crescer para guia operacional mais amplo ou se o fluxo minimo oficial passar a depender de Docker/runtime completo.

## Status final da frente

- `READY_FOR_COMMIT`
