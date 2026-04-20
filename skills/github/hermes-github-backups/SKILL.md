---
name: hermes-github-backups
description: Corrige e valida os backups Git do ecossistema Hermes — vault principal em hermes-wiki e backup sanitizado de skills/scripts/config de /root/.hermes.
version: 1.0.0
author: Hermes Agent
license: MIT
---

# Hermes GitHub Backups

Use esta skill quando precisar verificar, corrigir ou restaurar os backups Git do ambiente Hermes do Toni.

## Objetivo

Garantir dois fluxos distintos:
1. o vault principal do Obsidian em `/root/hermes-wiki`
2. um backup sanitizado de `/root/.hermes`

## Fonte de verdade atual

- Repositório do vault principal: `https://github.com/elvertoni/hermes-wiki.git`
- Repositório do backup sanitizado: `https://github.com/elvertoni/hermes-config-backup`

## Escopo do backup sanitizado

Inclui:
- `skills/`
- `scripts/`
- `config/config.redacted.yaml`

Exclui:
- tokens
- segredos
- sessões
- logs
- bancos locais
- estados efêmeros

## Scripts importantes

- `/root/.hermes/scripts/obsidian-auto-push.sh`
- `/root/.hermes/scripts/export-hermes-config-backup.py`
- `/root/.hermes/scripts/hermes-config-backup.sh`

## Fluxo de validação

### Vault principal
Verificar:
- remote do `hermes-wiki`
- branch atual
- `git status`
- se o último commit local bate com o head remoto

### Backup sanitizado
Verificar:
- se `config/config.redacted.yaml` existe
- se há `REDACTED` nos campos sensíveis
- se o repo local está limpo após export + commit + push
- se o head remoto bate com o local

## Resultado esperado

- mudanças no `hermes-wiki` sobem para o GitHub
- mudanças em skills, scripts e config sanitizada do Hermes sobem para o repositório privado separado
- segredos não entram no backup Git
