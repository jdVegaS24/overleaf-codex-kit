#!/usr/bin/env bash
set -euo pipefail

usage() {
  echo "Usage: bash ./setup-overleaf-project.sh GIT_URL [TARGET_DIR] [--no-credential-store]" >&2
}

if [[ $# -lt 1 ]]; then
  usage
  exit 2
fi

git_url="$1"
target_dir="${2:-}"
no_store=0

if [[ "${2:-}" == "--no-credential-store" ]]; then
  target_dir=""
  no_store=1
elif [[ "${3:-}" == "--no-credential-store" ]]; then
  no_store=1
fi

normalize_url() {
  local value="$1"
  value="${value#git clone }"
  value="${value%% *}"

  if [[ "$value" =~ ^https://www\.overleaf\.com/project/([^/?#[:space:]]+) ]]; then
    echo "https://git@git.overleaf.com/${BASH_REMATCH[1]}"
  elif [[ "$value" =~ ^https://git\.overleaf\.com/(.+)$ ]]; then
    echo "https://git@git.overleaf.com/${BASH_REMATCH[1]}"
  else
    echo "$value"
  fi
}

project_name_from_url() {
  local value="$1"
  local leaf="${value##*/}"
  if [[ -n "$leaf" ]]; then
    echo "overleaf-$leaf"
  else
    echo "overleaf-paper"
  fi
}

ensure_credential_helper() {
  local helper
  helper="$(git config --global --get credential.helper || true)"
  if [[ -n "$helper" ]]; then
    echo "Git credential helper: $helper"
    return
  fi

  if command -v git-credential-manager >/dev/null 2>&1; then
    git config --global credential.helper manager
    echo "Git credential helper configured: manager"
  elif command -v git-credential-osxkeychain >/dev/null 2>&1; then
    git config --global credential.helper osxkeychain
    echo "Git credential helper configured: osxkeychain"
  else
    echo "Warning: no secure Git credential helper found. Git may ask for the token on each operation." >&2
  fi
}

store_credential() {
  local url="$1"
  local host
  host="$(python3 -c 'import sys, urllib.parse; print(urllib.parse.urlparse(sys.argv[1]).hostname or "")' "$url" 2>/dev/null || true)"
  if [[ -z "$host" ]]; then
    host="$(printf '%s' "$url" | sed -E 's#https://([^/@]+@)?([^/]+)/.*#\2#')"
  fi

  ensure_credential_helper
  read -r -s -p "Paste your Overleaf Git token (hidden): " token
  echo
  printf 'protocol=https\nhost=%s\nusername=git\npassword=%s\n\n' "$host" "$token" | git credential approve
  unset token
  echo "Credential stored for $host with username git."
}

git --version

normalized_url="$(normalize_url "$git_url")"
if [[ -z "$target_dir" ]]; then
  target_dir="$(pwd)/$(project_name_from_url "$normalized_url")"
fi

if [[ "$no_store" != "1" ]]; then
  store_credential "$normalized_url"
fi

if [[ -e "$target_dir" ]]; then
  if [[ ! -d "$target_dir/.git" ]]; then
    echo "TARGET_DIR exists but is not a Git repository: $target_dir" >&2
    exit 1
  fi
  git -C "$target_dir" remote get-url origin >/dev/null 2>&1 \
    && git -C "$target_dir" remote set-url origin "$normalized_url" \
    || git -C "$target_dir" remote add origin "$normalized_url"
else
  git clone "$normalized_url" "$target_dir"
fi

git -C "$target_dir" config core.fileMode false

echo
echo "Repository ready at: $target_dir"
git -C "$target_dir" remote -v
git -C "$target_dir" status --short
echo
echo 'Open Codex in this folder and ask: Usa $overleaf-paper-sync para editar y subir los cambios a Overleaf.'
