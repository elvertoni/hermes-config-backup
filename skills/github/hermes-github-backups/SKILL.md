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

## Achado operacional importante

`/root/.hermes` não é um repositório git.

Consequência prática:
- qualquer instrução do tipo `cd /root/.hermes && git add ... && git commit ... && git push ...` vai falhar
- o caminho correto para versionar skills e config sanitizada é o espelho git em `/root/hermes-config-backup`

Fluxo correto para mudanças em skills:
1. editar o arquivo real em `/root/.hermes/skills/...`
2. rodar `/root/.hermes/scripts/hermes-config-backup.sh`
3. verificar o commit/push em `/root/hermes-config-backup`

Use esse fluxo especialmente quando algum prompt assumir incorretamente que `/root/.hermes` é versionado diretamente.

## Achados operacionais importantes

- O auto-push do vault principal pode parecer configurado, mas estar quebrado se o script ainda apontar para um path antigo como `/root/Documents/Obsidian Vault`.
- No ambiente validado, o path correto do vault principal é `/root/hermes-wiki`.
- O repositório sanitizado de `/root/.hermes` deve ser separado do vault principal para não misturar conhecimento editorial com configuração operacional.
- Ao criar o repo `hermes-config-backup`, `git clone https://github.com/...` pode falhar com `Repository not found` mesmo após `gh repo create`; no ambiente validado, `gh repo clone elvertoni/hermes-config-backup /root/hermes-config-backup` foi o caminho funcional.

## Cron esperado

```cron
*/5 * * * * /root/.hermes/scripts/obsidian-auto-push.sh
*/5 * * * * /root/.hermes/scripts/hermes-config-backup.sh >> /tmp/hermes-config-backup.log 2>&1
```

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
