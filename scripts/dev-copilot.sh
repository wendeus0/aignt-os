#!/usr/bin/env bash
# scripts/dev-copilot.sh
# Inicia o ambiente isolado do Copilot CLI dentro do devcontainer do projeto.
#
# Fluxo:
#   1. Sobe o serviço copilot-dev (docker compose -f compose.copilot.yaml)
#   2. Copia ~/.copilot/config.json para a tmpfs do container (auth isolada)
#   3. Executa `copilot` interativo dentro do container
#
# Uso:   ./scripts/dev-copilot.sh [--build] [-- <copilot-args>]
# Alias: alias sonnet='cd ~/work/projects/aignt-os && ./scripts/dev-copilot.sh'
set -euo pipefail

ROOT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
SERVICE="copilot-dev"
BUILD=0
COPILOT_BIN="${COPILOT_BIN:-${HOME}/.local/bin/copilot}"
COPILOT_CONFIG="${COPILOT_CONFIG:-${HOME}/.copilot/config.json}"

export DOCKER_CONFIG="${DOCKER_CONFIG:-${ROOT_DIR}/.cache/docker/config}"
export AIGNT_DEV_UID="${AIGNT_DEV_UID:-$(id -u)}"
export AIGNT_DEV_GID="${AIGNT_DEV_GID:-$(id -g)}"
export COPILOT_BIN

mkdir -p "${DOCKER_CONFIG}"

usage() {
  cat <<'EOF'
Usage: ./scripts/dev-copilot.sh [--build] [-- <copilot-args...>]

Inicia o Copilot CLI dentro do devcontainer isolado (read-only FS, cap_drop ALL).

Opções:
  --build    Reconstrói a imagem antes de subir o container.
  --help     Exibe esta mensagem.

Alias sugerido (adicionar ao ~/.bashrc ou ~/.zshrc):
  alias sonnet='cd ~/work/projects/aignt-os && ./scripts/dev-copilot.sh'
EOF
}

while [[ $# -gt 0 ]]; do
  case "$1" in
    --build)
      BUILD=1
      shift
      ;;
    --help|-h)
      usage
      exit 0
      ;;
    --)
      shift
      break
      ;;
    *)
      break
      ;;
  esac
done

# Verifica pré-requisitos
if [[ ! -x "${COPILOT_BIN}" ]]; then
  echo "ERRO: binário do Copilot não encontrado em '${COPILOT_BIN}'." >&2
  echo "  Defina COPILOT_BIN=<caminho> ou instale o Copilot CLI." >&2
  exit 1
fi

if [[ ! -f "${COPILOT_CONFIG}" ]]; then
  echo "ERRO: config do Copilot não encontrada em '${COPILOT_CONFIG}'." >&2
  echo "  Execute 'copilot auth login' no host antes de usar este script." >&2
  exit 1
fi

compose_cmd=(docker compose -f "${ROOT_DIR}/compose.copilot.yaml")
up_cmd=("${compose_cmd[@]}" up --detach)

[[ "${BUILD}" -eq 1 ]] && up_cmd+=(--build)
up_cmd+=("${SERVICE}")

# Sobe o container em silêncio; redireciona todo o output para evitar
# que mensagens do docker se misturem com a UI do Copilot.
if ! "${up_cmd[@]}" > /tmp/copilot-up.log 2>&1; then
  echo "ERRO: falha ao subir ${SERVICE}. Log:" >&2
  cat /tmp/copilot-up.log >&2
  exit 1
fi

# Copia o config de auth para a tmpfs via stdin (docker exec respeita a tmpfs;
# docker cp usa o overlay FS e falha com read_only: true)
"${compose_cmd[@]}" exec -T "${SERVICE}" \
  bash -c 'cat > /home/codex/.copilot/config.json && chmod 600 /home/codex/.copilot/config.json' \
  < "${COPILOT_CONFIG}" \
  > /dev/null 2>&1

# Injeta permissions-config.json pre-aprovando /workspace para eliminar
# o prompt "Confirm folder trust" a cada sessão.
"${compose_cmd[@]}" exec -T "${SERVICE}" \
  bash -c 'cat > /home/codex/.copilot/permissions-config.json && chmod 600 /home/codex/.copilot/permissions-config.json' \
  > /dev/null 2>&1 <<'PERMS'
{"locations":{"/workspace":{"tool_approvals":[{"kind":"write"},{"kind":"commands","commandIdentifiers":["*"]}]}}}
PERMS

# Limpa a tela antes de entregar o terminal ao Copilot, garantindo
# uma experiência idêntica à de abrir uma nova aba de terminal.
clear

# Executa o Copilot interativo
# --add-dir /workspace : pre-autoriza o workspace para acesso a arquivos
# --no-alt-screen      : desativa o buffer alternativo (melhor renderizacao via docker exec)
# TERM via -e          : herda o tipo de terminal do host
exec_cmd=(
  "${compose_cmd[@]}"
  exec
  -e "TERM=${TERM:-xterm-256color}"
  "${SERVICE}"
  /usr/local/bin/copilot
  --add-dir /workspace
  --no-alt-screen
)

[[ $# -gt 0 ]] && exec_cmd+=("$@")

exec "${exec_cmd[@]}"
