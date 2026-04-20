#!/bin/bash
# Auto-commit and push changes in Obsidian vault
# Runs via cron every 5 minutes

VAULT="/root/hermes-wiki"
BRANCH="main"
LOG="/tmp/obsidian-auto-push.log"

cd "$VAULT" || exit 1

# Check for changes
if git diff --quiet --cached && git diff --quiet && [ -z "$(git ls-files --others --exclude-standard)" ]; then
    exit 0
fi

# Stage all changes
git add -A

# Check again after staging
if git diff --cached --quiet; then
    exit 0
fi

# Commit with timestamp
TIMESTAMP=$(date '+%Y-%m-%d %H:%M')
git commit -m "auto: $TIMESTAMP" --quiet 2>>"$LOG"

# Push
git push origin "$BRANCH" --quiet 2>>"$LOG"

echo "[$(date)] pushed changes" >> "$LOG"
