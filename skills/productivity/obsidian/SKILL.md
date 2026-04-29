---
name: obsidian
description: Manage Toni's Obsidian Hermes Vault using the Karpathy LLM Wiki pattern. Use this skill for explicit requests to save, publish, ingest, organize, query, audit, migrate, or update durable knowledge in `/root/hermes-vault`, Obsidian, the Hermes vault, raw sources, the compiled wiki, DEV, PROF, HERMES, second brain work, or Notion-to-Obsidian migration.
version: 1.1.0
author: Toni Coimbra + Hermes
license: MIT
metadata:
  hermes:
    tags: [obsidian, hermes-vault, llm-wiki, second-brain, markdown, syncthing, knowledge-base]
    homepage: /root/hermes-vault
    related_skills: [notion, hermes-agent, codex]
---

# Obsidian Hermes Vault

Operate Toni's Obsidian vault at:

```text
/root/hermes-vault
```

This vault follows Andrej Karpathy's LLM Wiki pattern:

- `raw/` is immutable source material.
- `wiki/` is the compiled markdown wiki maintained by the LLM.
- `AGENTS.md` is the schema and operating contract.
- Obsidian is the IDE/frontend.

Before creating or editing vault content, read:

```text
/root/hermes-vault/AGENTS.md
```

For detailed conventions, read only the needed reference:

- `references/vault-contract.md`: structure, domains, frontmatter, naming.
- `references/migration-sync.md`: Notion migration, Syncthing safety, validation commands.

## Core Rules

- Preserve original sources in `raw/`.
- Put compiled durable knowledge in `wiki/`.
- Keep runtime outside the vault: no `.venv`, packages, tests, caches, or build artifacts.
- Update existing wiki pages before creating new pages.
- Keep `wiki/index.md` current after meaningful changes.
- Append to `wiki/log.md`; do not rewrite history.
- Use Obsidian wikilinks and preserve source provenance.

## Domain Routing

- `wiki/DEV/`: development, AI, automation, programming, Linux, systems, tools, technical research.
- `wiki/PROF/`: teaching, SEED-PR, classes, lesson planning, classroom activities, professional references.
- `wiki/HERMES/`: Hermes agent memory, architecture, prompts, automations, operating decisions, workflows.

## Ingest Workflow

Use when Toni sends an article, link, document, note, export, repo, paper, image, transcript, or says to "jogar no vault", "publicar no Obsidian", "salvar no Hermes", or "organizar isso".

1. Read `/root/hermes-vault/AGENTS.md`.
2. Confirm or save the original source under `raw/`.
3. Read `references/vault-contract.md` if creating or updating wiki pages.
4. Search `wiki/index.md` and relevant domain folders before writing.
5. Extract reusable ideas, entities, decisions, tools, commands, contradictions, and source metadata.
6. Update existing pages first.
7. Create new pages only for durable knowledge.
8. Update `wiki/index.md`.
9. Append one entry to `wiki/log.md`:

```markdown
## [YYYY-MM-DD] ingest | Source or topic title

- Source: [[raw/articles/example]]
- Updated: [[wiki/DEV/example-page]]
- Created: [[wiki/HERMES/example-decision]]
- Notes: concise summary of what changed.
```

## Query Workflow

Use when Toni asks questions against his knowledge base or wants Hermes to consult the vault.

1. Read `wiki/index.md` first.
2. Read relevant pages in `wiki/DEV`, `wiki/PROF`, and `wiki/HERMES`.
3. Read raw sources only when provenance, quotes, images, or missing detail matter.
4. Answer with internal wikilinks.
5. Separate what the vault says, what Hermes infers, and what is missing or stale.
6. File durable answers into a domain page or `wiki/outputs/`.
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

- markdown report: `wiki/outputs/markdown/`
- Marp slide deck: `wiki/outputs/marp/`
- chart/image from analysis: `wiki/outputs/charts/`
- canvas or visual map: `wiki/outputs/canvas/`

Valuable outputs should later be integrated into domain pages and linked back.

## Response Style

When completing an Obsidian task, report:

- files created;
- files updated;
- raw sources preserved;
- index/log updates;
- uncertainty or follow-up needed.

Keep the response concise. The important artifact is the updated vault.
