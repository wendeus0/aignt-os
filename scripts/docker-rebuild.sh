#!/usr/bin/env bash
set -euo pipefail

ROOT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
STATE_FILE="$ROOT_DIR/.cache/docker/rebuild.sha256"
TAG="synapse-os:dev"
USE_COMPOSE=0
FORCE=0
DRY_RUN=0
PRINT_FILES=0
CHECK_ONLY=0
NO_CACHE=0

RELEVANT_PATHS=(
  "src"
  "pyproject.toml"
  "uv.lock"
  "Dockerfile"
  ".dockerignore"
  "compose.yaml"
  "docker-compose.yml"
  "scripts"
  ".python-version"
)

while [[ $# -gt 0 ]]; do
  case "$1" in
    --state-file)
      STATE_FILE="${2:?missing value for --state-file}"
      shift 2
      ;;
    --tag)
      TAG="${2:?missing value for --tag}"
      shift 2
      ;;
    --use-compose)
      USE_COMPOSE=1
      shift
      ;;
    --force)
      FORCE=1
      shift
      ;;
    --dry-run)
      DRY_RUN=1
      shift
      ;;
    --print-files)
      PRINT_FILES=1
      shift
      ;;
    --check-only)
      CHECK_ONLY=1
      shift
      ;;
    --no-cache)
      NO_CACHE=1
      shift
      ;;
    *)
      echo "Unknown argument: $1" >&2
      exit 1
      ;;
  esac
done

list_files() {
  if git -C "$ROOT_DIR" rev-parse --is-inside-work-tree >/dev/null 2>&1; then
    git -C "$ROOT_DIR" ls-files -- "${RELEVANT_PATHS[@]}" | sort -u
    return
  fi

  for path in "${RELEVANT_PATHS[@]}"; do
    if [[ -d "$ROOT_DIR/$path" ]]; then
      find "$ROOT_DIR/$path" -type f -printf '%P\n'
    elif [[ -f "$ROOT_DIR/$path" ]]; then
      printf '%s\n' "$path"
    fi
  done | sort -u
}

compute_fingerprint() {
  local file
  while IFS= read -r file; do
    [[ -n "$file" ]] || continue
    sha256sum "$ROOT_DIR/$file"
  done < <(list_files) | sha256sum | awk '{print $1}'
}

if [[ "$PRINT_FILES" -eq 1 ]]; then
  list_files
  exit 0
fi

current_fingerprint="$(compute_fingerprint)"
stored_fingerprint=""

if [[ -f "$STATE_FILE" ]]; then
  stored_fingerprint="$(tr -d '[:space:]' < "$STATE_FILE")"
fi

if [[ "$FORCE" -eq 1 || "$current_fingerprint" != "$stored_fingerprint" ]]; then
  rebuild_required=1
else
  rebuild_required=0
fi

printf '%s\n' "Fingerprint: $current_fingerprint"

if [[ "$rebuild_required" -eq 0 ]]; then
  printf '%s\n' "No relevant changes detected. Rebuild skipped."
  exit 0
fi

printf '%s\n' "Relevant changes detected. Rebuild required."

if [[ "$CHECK_ONLY" -eq 1 ]]; then
  exit 0
fi

build_args=(--tag "$TAG")
if [[ "$USE_COMPOSE" -eq 1 ]]; then
  build_args+=(--use-compose)
fi
if [[ "$NO_CACHE" -eq 1 ]]; then
  build_args+=(--no-cache)
fi
if [[ "$DRY_RUN" -eq 1 ]]; then
  build_args+=(--dry-run)
fi

"$ROOT_DIR/scripts/docker-build.sh" "${build_args[@]}"

if [[ "$DRY_RUN" -eq 0 ]]; then
  mkdir -p "$(dirname "$STATE_FILE")"
  printf '%s\n' "$current_fingerprint" > "$STATE_FILE"
fi
