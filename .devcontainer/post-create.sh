#!/usr/bin/env bash
set -euo pipefail

WORKSPACE_DIR="${WORKSPACE_DIR:-/workspace}"
HOME_DIR="${HOME:-/home/codex}"
PROJECT_CODEX_DIR="$WORKSPACE_DIR/.codex"
RUNTIME_CODEX_DIR="$HOME_DIR/.codex"

mkdir -p \
  "$PROJECT_CODEX_DIR" \
  "$RUNTIME_CODEX_DIR" \
  "$HOME_DIR/.cache/uv" \
  "$HOME_DIR/.local/state" \
  "$HOME_DIR/.local/share"

ln -snf "$PROJECT_CODEX_DIR/config.toml" "$RUNTIME_CODEX_DIR/config.toml"

printf '%s\n' "Codex dev container ready."
printf '%s\n' "Project config linked from $PROJECT_CODEX_DIR/config.toml"
