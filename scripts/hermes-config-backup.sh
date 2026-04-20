#!/bin/bash
set -e
EXPORTER="/root/.hermes/scripts/export-hermes-config-backup.py"
REPO="/root/hermes-config-backup"
BRANCH="main"
LOG="/tmp/hermes-config-backup.log"

python3 "$EXPORTER" >>"$LOG" 2>&1
cd "$REPO" || exit 1

if git diff --quiet --cached && git diff --quiet && [ -z "$(git ls-files --others --exclude-standard)" ]; then
    exit 0
fi

git add -A

if git diff --cached --quiet; then
    exit 0
fi

TIMESTAMP=$(date '+%Y-%m-%d %H:%M')
git commit -m "backup: $TIMESTAMP" --quiet 2>>"$LOG"
git push origin "$BRANCH" --quiet 2>>"$LOG"
echo "[$(date)] backup pushed" >> "$LOG"
