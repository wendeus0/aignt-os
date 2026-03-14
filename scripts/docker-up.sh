#!/usr/bin/env bash
set -euo pipefail

ROOT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
SERVICE="synapse-os"
DETACH=0
BUILD=0
DRY_RUN=0
APP_UID="${SYNAPSE_OS_UID:-$(id -u)}"
APP_GID="${SYNAPSE_OS_GID:-$(id -g)}"

export DOCKER_CONFIG="${DOCKER_CONFIG:-$ROOT_DIR/.cache/docker/config}"
export SYNAPSE_OS_UID="$APP_UID"
export SYNAPSE_OS_GID="$APP_GID"
mkdir -p "$DOCKER_CONFIG"

require_docker() {
  if ! command -v docker >/dev/null 2>&1; then
    echo "Docker CLI is required to start the container." >&2
    exit 1
  fi

  if ! docker version >/dev/null 2>&1; then
    echo "Docker daemon is not accessible. Check docker.sock permissions or start the daemon." >&2
    exit 1
  fi
}

while [[ $# -gt 0 ]]; do
  case "$1" in
    --service)
      SERVICE="${2:?missing value for --service}"
      shift 2
      ;;
    --detach)
      DETACH=1
      shift
      ;;
    --build)
      BUILD=1
      shift
      ;;
    --dry-run)
      DRY_RUN=1
      shift
      ;;
    *)
      echo "Unknown argument: $1" >&2
      exit 1
      ;;
  esac
done

up_cmd=(docker compose -f "$ROOT_DIR/compose.yaml" up)
if [[ "$DETACH" -eq 1 ]]; then
  up_cmd+=(--detach)
fi
if [[ "$BUILD" -eq 1 ]]; then
  up_cmd+=(--build)
fi
up_cmd+=("$SERVICE")

printf '%s\n' "Resolved up command: ${up_cmd[*]}"

if [[ "$DRY_RUN" -eq 1 ]]; then
  exit 0
fi

require_docker
"${up_cmd[@]}"
