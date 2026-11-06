#!/usr/bin/env bash
set -euo pipefail

# 技能名派生自目录本身：本脚本位于 <skill>/scripts/，技能目录即自包含安装单元
SOURCE_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
SKILL_NAME="$(basename "$SOURCE_DIR")"
TARGET="${1:-}"
PROJECT_ROOT="${2:-$(pwd)}"

usage() {
  printf '%s\n' \
    "Usage: $0 <target> [project-root-or-custom-skills-dir]" \
    "Targets: codex-global, codex-project, claude-global, claude-project," \
    "         openclaw-global, openclaw-workspace, all-global, custom"
}

if [[ "$TARGET" == "all-global" ]]; then
  TARGET_ROOTS=(
    "${CODEX_HOME:-$HOME/.codex}/skills"
    "$HOME/.claude/skills"
    "${OPENCLAW_WORKSPACE:-$HOME/.openclaw/workspace}/skills"
  )
  for root in "${TARGET_ROOTS[@]}"; do
    destination="$root/$SKILL_NAME"
    if [[ -e "$destination" || -L "$destination" ]]; then
      printf 'Refusing partial install; existing path: %s\n' "$destination" >&2
      exit 3
    fi
  done
  for root in "${TARGET_ROOTS[@]}"; do
    mkdir -p "$root"
    ln -s "$SOURCE_DIR" "$root/$SKILL_NAME"
    printf 'Installed %s -> %s\n' "$root/$SKILL_NAME" "$SOURCE_DIR"
  done
  exit 0
fi

case "$TARGET" in
  codex-global)
    TARGET_ROOT="${CODEX_HOME:-$HOME/.codex}/skills"
    ;;
  codex-project)
    TARGET_ROOT="$PROJECT_ROOT/.agents/skills"
    ;;
  claude-global)
    TARGET_ROOT="$HOME/.claude/skills"
    ;;
  claude-project)
    TARGET_ROOT="$PROJECT_ROOT/.claude/skills"
    ;;
  openclaw-global)
    TARGET_ROOT="${OPENCLAW_HOME:-$HOME/.openclaw}/skills"
    ;;
  openclaw-workspace)
    TARGET_ROOT="${OPENCLAW_WORKSPACE:-$HOME/.openclaw/workspace}/skills"
    ;;
  custom)
    if [[ $# -lt 2 ]]; then
      usage
      exit 2
    fi
    TARGET_ROOT="$2"
    ;;
  *)
    usage
    exit 2
    ;;
esac

DESTINATION="$TARGET_ROOT/$SKILL_NAME"
mkdir -p "$TARGET_ROOT"

if [[ -e "$DESTINATION" || -L "$DESTINATION" ]]; then
  printf 'Refusing to replace existing path: %s\n' "$DESTINATION" >&2
  exit 3
fi

ln -s "$SOURCE_DIR" "$DESTINATION"
printf 'Installed %s -> %s\n' "$DESTINATION" "$SOURCE_DIR"
