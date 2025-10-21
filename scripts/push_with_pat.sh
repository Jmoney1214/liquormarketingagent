#!/usr/bin/env bash
set -euo pipefail
OWNER="${1:-}"; REPO="${2:-}"; PRIVATE="${3:-true}"; TOKEN="${GITHUB_TOKEN:-}"
if [[ -z "$OWNER" || -z "$REPO" || -z "$TOKEN" ]]; then echo "Usage: GITHUB_TOKEN=xxxx $0 <owner> <repo> [private:true|false]"; exit 1; fi
SCRIPT_DIR="$( cd -- "$( dirname -- "${BASH_SOURCE[0]}" )" &> /dev/null && pwd )"
cd "$SCRIPT_DIR/.."
curl -sf -H "Authorization: token $TOKEN" -H "Accept: application/vnd.github+json" -d "{"name":"$REPO","private":$PRIVATE}" https://api.github.com/user/repos >/dev/null
git init; git add .; git commit -m "init: liquor marketing agent" || true; git branch -M main
git remote add origin "https://$TOKEN@github.com/$OWNER/$REPO.git" || git remote set-url origin "https://$TOKEN@github.com/$OWNER/$REPO.git"
git push -u origin main; git remote set-url origin "https://github.com/$OWNER/$REPO.git"
echo "✅ https://github.com/$OWNER/$REPO"
