# Migration And Sync

## Notion Migration

When migrating from Notion:

1. Preserve the raw export or extracted page content under `raw/`.
2. Do not mirror Notion's nested structure blindly.
3. Reclassify content into `wiki/DEV`, `wiki/PROF`, or `wiki/HERMES`.
4. Merge duplicates and old fragments into durable pages.
5. Keep source provenance pointing back to the raw export.
6. Update `wiki/index.md` and `wiki/log.md`.

## Syncthing Safety

The vault is synced across VPS, Dell G15, and S24.

Current folder:

```text
Folder ID: hermes-llm-wiki-20260429
Label: hermes-vault
Path: /root/hermes-vault
```

Rules:

- Avoid writing large temporary files inside the vault.
- Avoid editing Obsidian workspace state.
- Do not accept or recreate old folder IDs such as `llm-wiki` or older `hermes-vault` IDs.
- If conflict files appear, inspect both versions and merge intentionally.
- Keep `.stignore` aligned with the rule that runtime does not belong in the vault.
- Check Syncthing API status only when `SYNCTHING_API_KEY` is already available.
- Never print, log, paste, or store the Syncthing API key in chat or vault files.

Filesystem checks:

```bash
find /root/hermes-vault -maxdepth 4 | sort
find /root/hermes-vault \( -name '.venv' -o -name 'llm_wiki' -o -name 'tests' -o -name '*sync-conflict*' -o -name 'requirements.txt' -o -name 'pyproject.toml' -o -name '__pycache__' \) | sort
```

API check, only if the key is already in the environment:

```bash
curl -s -H "X-API-Key: $SYNCTHING_API_KEY" \
  "http://127.0.0.1:8384/rest/db/status?folder=hermes-llm-wiki-20260429"
```
