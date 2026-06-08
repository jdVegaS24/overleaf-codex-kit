#!/usr/bin/env bash
set -euo pipefail

force=0
codex_home="${CODEX_HOME:-$HOME/.codex}"

while [[ $# -gt 0 ]]; do
  case "$1" in
    --force)
      force=1
      shift
      ;;
    --codex-home)
      codex_home="$2"
      shift 2
      ;;
    *)
      echo "Usage: bash ./install.sh [--force] [--codex-home PATH]" >&2
      exit 2
      ;;
  esac
done

script_dir="$(cd -- "$(dirname -- "${BASH_SOURCE[0]}")" && pwd)"
skill_name="overleaf-paper-sync"
source_dir="$script_dir/skills/$skill_name"
dest_root="$codex_home/skills"
dest_dir="$dest_root/$skill_name"

if [[ ! -f "$source_dir/SKILL.md" ]]; then
  echo "Skill not found at: $source_dir" >&2
  exit 1
fi

mkdir -p "$dest_root"

if [[ -e "$dest_dir" ]]; then
  if [[ "$force" != "1" ]]; then
    echo "Skill already exists at $dest_dir. Re-run with --force to replace it." >&2
    exit 1
  fi
  rm -rf "$dest_dir"
fi

cp -R "$source_dir" "$dest_dir"

echo "Skill installed at: $dest_dir"
echo "Restart Codex or open a new thread if the skill does not appear immediately."
