#!/usr/bin/env bash
set -euo pipefail
OWNER="${1:-}"; REPO="${2:-}"; VIS="${3:---private}"
if [[ -z "$OWNER" || -z "$REPO" ]]; then echo "Usage: $0 <owner> <repo> [--public|--private]"; exit 1; fi
SCRIPT_DIR="$( cd -- "$( dirname -- "${BASH_SOURCE[0]}" )" &> /dev/null && pwd )"
cd "$SCRIPT_DIR/.."
git init; git add .; git commit -m "init: liquor marketing agent" || true; git branch -M main
gh repo create "$OWNER/$REPO" "$VIS" --source . --remote origin --push
echo "✅ https://github.com/$OWNER/$REPO"
