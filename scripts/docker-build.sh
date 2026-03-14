#!/usr/bin/env bash
set -euo pipefail

ROOT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
TAG="synapse-os:dev"
USE_COMPOSE=0
NO_CACHE=0
DRY_RUN=0
APP_UID="${SYNAPSE_OS_UID:-$(id -u)}"
APP_GID="${SYNAPSE_OS_GID:-$(id -g)}"

export DOCKER_CONFIG="${DOCKER_CONFIG:-$ROOT_DIR/.cache/docker/config}"
export SYNAPSE_OS_UID="$APP_UID"
export SYNAPSE_OS_GID="$APP_GID"
mkdir -p "$DOCKER_CONFIG"

require_docker() {
  if ! command -v docker >/dev/null 2>&1; then
    echo "Docker CLI is required to build the container." >&2
    exit 1
  fi

  if ! docker version >/dev/null 2>&1; then
    echo "Docker daemon is not accessible. Check docker.sock permissions or start the daemon." >&2
    exit 1
  fi
}

while [[ $# -gt 0 ]]; do
  case "$1" in
    --tag)
      TAG="${2:?missing value for --tag}"
      shift 2
      ;;
    --use-compose)
      USE_COMPOSE=1
      shift
      ;;
    --no-cache)
      NO_CACHE=1
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

build_cmd=(
  docker build
  --build-arg "APP_UID=$APP_UID"
  --build-arg "APP_GID=$APP_GID"
  --file "$ROOT_DIR/Dockerfile"
  --tag "$TAG"
)
if [[ "$NO_CACHE" -eq 1 ]]; then
  build_cmd+=(--no-cache)
fi
build_cmd+=("$ROOT_DIR")

compose_cmd=(docker compose -f "$ROOT_DIR/compose.yaml" build)
if [[ "$NO_CACHE" -eq 1 ]]; then
  compose_cmd+=(--no-cache)
fi
compose_cmd+=(synapse-os)

if [[ "$USE_COMPOSE" -eq 1 ]]; then
  selected_cmd=("${compose_cmd[@]}")
else
  selected_cmd=("${build_cmd[@]}")
fi

printf '%s\n' "Resolved build command: ${selected_cmd[*]}"

if [[ "$DRY_RUN" -eq 1 ]]; then
  exit 0
fi

require_docker
"${selected_cmd[@]}"
