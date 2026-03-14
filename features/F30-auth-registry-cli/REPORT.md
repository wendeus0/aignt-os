# F30 Report

## Resumo executivo

- A F30 removeu a edicao manual do auth registry introduzido na F29, adicionando uma CLI local para bootstrap, emissao e disable de tokens.
- O recorte permaneceu estritamente local: o Synapse-Flow continua sendo a engine propria de pipeline do SynapseOS e a frente nao abriu socket, auth remota ou RBAC distribuido.
- O backlog documental tambem foi alinhado ao baseline pos-F28/F29/F30, deixando `docs/IDEAS.md` coerente com o estado real do repositorio.

## Escopo entregue

- Novo grupo `synapse auth` com:
  - `auth init` para criar registry novo e emitir o primeiro token
  - `auth issue` para emitir token para principal existente ou criar principal novo com role explicita
  - `auth disable` para revogar token por `token_id`
- `src/synapse_os/auth.py` ampliado com:
  - `token_id` por token persistido
  - operacoes explicitas de inicializacao, emissao e disable
  - compatibilidade com registries antigos sem `token_id`
- `src/synapse_os/cli/app.py` ampliado com o novo grupo publico `auth`
- README atualizado com o fluxo local `init -> issue -> disable`
- `docs/IDEAS.md` atualizado para refletir `F28`, `F29` e `F30`
- cobertura unitaria e de integracao para lifecycle local de tokens

## Validacoes executadas

- Validacao da SPEC com `validate_spec_file(Path('features/F30-auth-registry-cli/SPEC.md'))`
- `env UV_CACHE_DIR=/home/g0dsssp33d/work/projects/synapse-os/.cache/uv uv run --no-sync python -m pytest tests/unit/test_auth.py tests/integration/test_cli_auth_registry.py tests/integration/test_cli_auth_rbac.py tests/unit/test_auth_registry_docs.py -q`
- `env UV_CACHE_DIR=/home/g0dsssp33d/work/projects/synapse-os/.cache/uv uv run --no-sync ruff check src/synapse_os/auth.py src/synapse_os/cli/app.py tests/unit/test_auth.py tests/integration/test_cli_auth_registry.py tests/unit/test_auth_registry_docs.py`
- `env UV_CACHE_DIR=/home/g0dsssp33d/work/projects/synapse-os/.cache/uv uv run --no-sync python -m mypy src/synapse_os/auth.py src/synapse_os/cli/app.py`
- `./scripts/commit-check.sh --no-sync --skip-branch-validation --skip-docker --skip-security --skip-format`
- `./scripts/security-gate.sh`

## Review de seguranca

- Parecer final: aprovado.
- Riscos revisados:
  - vazamento de token bruto em disco ou erro publico
  - disable inefetivo com token ainda autenticando
  - ampliacao acidental da auth para comandos de leitura
  - drift documental entre README, backlog e superficie publica
- Mitigacoes aplicadas:
  - o registry persiste apenas `token_sha256`, `token_id`, `principal_id` e `disabled`
  - o token bruto so aparece no stdout nominal de `init` e `issue`
  - `disable` faz `authenticate()` ignorar o token marcado como desabilitado
  - README e `docs/IDEAS.md` foram atualizados no mesmo delta

## Riscos residuais

- O registry continua local ao host/workspace atual, sem coordenacao entre processos ou hosts.
- Nao ha listagem administrativa completa de principals ou tokens; o recorte ficou deliberadamente pequeno.
- A verificacao global de `ruff format --check .` continua com debt preexistente fora do escopo da F30; os arquivos tocados por esta frente estao formatados.

## Proximos passos

- Rodar `branch-sync-guard` antes de commit/push/PR.
- Abrir PR da F30 com foco no boundary local da auth registry CLI.
- Manter operacao remota de `G-11` explicitamente adiada ate uma SPEC propria.

## Status final da frente

- `READY_FOR_COMMIT`
