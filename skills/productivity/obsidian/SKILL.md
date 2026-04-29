---
name: obsidian
description: Manage Toni's Obsidian Hermes Vault using the Karpathy LLM Wiki pattern. Use this skill whenever the user asks to save, publish, ingest, organize, query, audit, migrate, summarize, clip, file, or update knowledge in Obsidian, the Hermes vault, the wiki, raw sources, DEV, PROF, HERMES, second brain, articles, notes, study material, or Notion-to-Obsidian migration. This skill is the default for any request that should become durable knowledge for Hermes or Toni.
version: 1.0.0
author: Toni Coimbra + Hermes
license: MIT
metadata:
  hermes:
    tags: [obsidian, hermes-vault, llm-wiki, second-brain, markdown, syncthing, knowledge-base]
    homepage: /root/hermes-vault
    related_skills: [notion, hermes-agent, codex]
---

# Obsidian Hermes Vault

Use this skill to operate Toni's Obsidian vault at:

```text
/root/hermes-vault
```

This vault follows Andrej Karpathy's LLM Wiki pattern:

- `raw/` is immutable source material.
- `wiki/` is the compiled markdown wiki maintained by the LLM.
- `AGENTS.md` is the schema and operating contract.
- Obsidian is the IDE/frontend.
- Hermes/Codex maintains the wiki; Toni curates sources, reviews outputs, and asks questions.

Before creating or editing vault content, read:

```text
/root/hermes-vault/AGENTS.md
```

## Current Structure

```text
/root/hermes-vault/
  AGENTS.md
  README.md
  raw/
    inbox/
    articles/
    papers/
    repos/
    datasets/
    images/
    assets/
  wiki/
    DEV/
    PROF/
    HERMES/
    outputs/
      markdown/
      marp/
      charts/
      canvas/
    templates/
    index.md
    log.md
  .obsidian/
  .stignore
```

Syncthing folder:

```text
Folder ID: hermes-llm-wiki-20260429
Label: hermes-vault
Path: /root/hermes-vault
Devices: VPS, TONI_G15, s24+
```

## Operating Principles

- Treat `raw/` as source of truth. Do not rewrite or delete raw sources after ingest.
- Treat `wiki/` as compiled knowledge. Hermes owns this layer.
- Keep runtime outside the vault. Do not place `.venv`, code packages, tests, caches, or build artifacts in `/root/hermes-vault`.
- Prefer updating existing wiki pages before creating new ones.
- Preserve source provenance in frontmatter and body links.
- Maintain `wiki/index.md` on every meaningful ingest or durable update.
- Maintain `wiki/log.md` as append-only chronological history.
- Use Obsidian wikilinks for internal references.

## Domain Routing

Classify durable knowledge into one primary domain:

- `wiki/DEV/`: development, AI, automation, programming, Linux, systems, tools, technical research.
- `wiki/PROF/`: teaching, SEED-PR, classes, lesson planning, classroom activities, professional references.
- `wiki/HERMES/`: Hermes agent memory, architecture, prompts, automations, operating decisions, workflows.

If a source spans multiple domains, pick the main destination and add cross-links to related domain pages.

## Frontmatter Contract

Every durable page in `wiki/DEV`, `wiki/PROF`, or `wiki/HERMES` must begin with YAML:

```yaml
---
title: "Clear title"
domain: dev
type: concept
status: draft
created: 2026-04-29
updated: 2026-04-29
tags:
  - dev
sources:
  - "[[raw/articles/example]]"
related:
  - "[[Related page]]"
---
```

Allowed `domain` values:

- `dev`
- `prof`
- `hermes`

Allowed `type` values:

- `summary`
- `concept`
- `entity`
- `tool`
- `project`
- `decision`
- `prompt`
- `lesson`
- `comparison`
- `reference`
- `output`

Allowed `status` values:

- `draft`
- `active`
- `evergreen`
- `archived`

## File Naming

- Use kebab-case filenames.
- Use ASCII-only filenames.
- Prefer stable concept names over dated names.
- Use dates only for logs, snapshots, events, lessons, and time-specific outputs.

Examples:

```text
wiki/DEV/github-ssh-duas-contas.md
wiki/PROF/atividade-logica-programacao-listas.md
wiki/HERMES/syncthing-vault-operacao.md
raw/articles/2026-04-29-karpathy-llm-knowledge-bases.md
```

## Ingest Workflow

Use when Toni sends an article, link, document, note, export, repo, paper, image, transcript, or says to "jogar no vault", "publicar no Obsidian", "salvar no Hermes", "organizar isso", or similar.

1. Read `/root/hermes-vault/AGENTS.md`.
2. Save or confirm the original source under `raw/`.
3. Choose the correct raw folder:
   - web article: `raw/articles/`
   - paper/PDF: `raw/papers/`
   - repo notes or code reference: `raw/repos/`
   - dataset: `raw/datasets/`
   - image/screenshot: `raw/images/` or `raw/assets/`
   - unclassified capture: `raw/inbox/`
4. Search `wiki/index.md` and relevant domain folders before writing.
5. Extract reusable ideas, entities, decisions, tools, commands, contradictions, and source metadata.
6. Update existing pages first.
7. Create new pages only for durable knowledge.
8. Use frontmatter and wikilinks.
9. Update `wiki/index.md`.
10. Append one entry to `wiki/log.md` using this format:

```markdown
## [YYYY-MM-DD] ingest | Source or topic title

- Source: [[raw/articles/example]]
- Updated: [[wiki/DEV/example-page]]
- Created: [[wiki/HERMES/example-decision]]
- Notes: concise summary of what changed.
```

## Query Workflow

Use when Toni asks questions against his knowledge base, asks what he already has, asks for a synthesis, or wants Hermes to consult the vault.

1. Read `wiki/index.md` first.
2. Read relevant pages in `wiki/DEV`, `wiki/PROF`, and `wiki/HERMES`.
3. Read raw sources only when provenance, quotes, images, or missing detail matter.
4. Answer with internal wikilinks.
5. Separate:
   - what the vault explicitly says;
   - what Hermes is inferring;
   - what is missing or stale.
6. If the answer is durable, file it as:
   - domain page in `wiki/DEV`, `wiki/PROF`, or `wiki/HERMES`; or
   - output in `wiki/outputs/markdown/`, `wiki/outputs/marp/`, `wiki/outputs/charts/`, or `wiki/outputs/canvas/`.
7. Update `wiki/index.md` and `wiki/log.md` if files changed.

## Lint Workflow

Use when Toni asks to review, audit, clean, validate, fix, health-check, or "ver se esta no padrao".

Check for:

- files outside the allowed structure;
- runtime artifacts inside the vault;
- missing or invalid frontmatter;
- broken wikilinks;
- orphan wiki pages;
- stale claims;
- raw sources without compiled wiki coverage;
- wiki pages without source provenance;
- important repeated concepts lacking pages;
- contradictions between pages;
- Syncthing conflict files.

Fix safe structural issues directly. Report risky content changes before rewriting meaning.

## Output Workflow

When Toni asks for an output from knowledge work:

- markdown report: `wiki/outputs/markdown/`
- Marp slide deck: `wiki/outputs/marp/`
- chart/image generated from analysis: `wiki/outputs/charts/`
- canvas or visual map: `wiki/outputs/canvas/`

If the output contains durable knowledge, later integrate it into a domain page and link back to the output.

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

- Avoid writing large temporary files inside the vault.
- Avoid editing Obsidian workspace state.
- Do not accept or recreate old folder IDs such as `llm-wiki` or older `hermes-vault` IDs.
- If conflict files appear, inspect both versions and merge intentionally.
- Keep `.stignore` aligned with the rule that runtime does not belong in the vault.

## Commands

Inspect tree:

```bash
find /root/hermes-vault -maxdepth 4 | sort
```

Find suspicious runtime artifacts:

```bash
find /root/hermes-vault \( -name '.venv' -o -name 'llm_wiki' -o -name 'tests' -o -name '*sync-conflict*' -o -name 'requirements.txt' -o -name 'pyproject.toml' -o -name '__pycache__' \) | sort
```

Check Syncthing folder status only when `SYNCTHING_API_KEY` is already available in the environment. Never print, log, paste, or store the Syncthing API key in chat or vault files.

```bash
curl -s -H "X-API-Key: $SYNCTHING_API_KEY" \
  "http://127.0.0.1:8384/rest/db/status?folder=hermes-llm-wiki-20260429"
```

If `$SYNCTHING_API_KEY` is not set, skip the API check and use local filesystem validation instead.

## Response Style

When completing an Obsidian task, report:

- files created;
- files updated;
- raw sources preserved;
- index/log updates;
- any uncertainty or follow-up needed.

Keep the response concise. The important artifact is the updated vault, not a long explanation.
