# Hermes Vault Contract

Vault path:

```text
/root/hermes-vault
```

Structure:

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

Operating principles:

- Treat `raw/` as source of truth. Do not rewrite or delete raw sources after ingest.
- Treat `wiki/` as compiled knowledge. Hermes owns this layer.
- Keep runtime outside the vault. Do not place `.venv`, code packages, tests, caches, or build artifacts in `/root/hermes-vault`.
- Prefer updating existing wiki pages before creating new ones.
- Preserve source provenance in frontmatter and body links.
- Maintain `wiki/index.md` on every meaningful ingest or durable update.
- Maintain `wiki/log.md` as append-only chronological history.
- Use Obsidian wikilinks for internal references.

Domains:

- `wiki/DEV/`: development, AI, automation, programming, Linux, systems, tools, technical research.
- `wiki/PROF/`: teaching, SEED-PR, classes, lesson planning, classroom activities, professional references.
- `wiki/HERMES/`: Hermes agent memory, architecture, prompts, automations, operating decisions, workflows.

Frontmatter:

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

Allowed `domain` values: `dev`, `prof`, `hermes`.

Allowed `type` values: `summary`, `concept`, `entity`, `tool`, `project`, `decision`, `prompt`, `lesson`, `comparison`, `reference`, `output`.

Allowed `status` values: `draft`, `active`, `evergreen`, `archived`.

Naming:

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
