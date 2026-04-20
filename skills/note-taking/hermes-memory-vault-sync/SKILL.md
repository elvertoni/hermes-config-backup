---
name: hermes-memory-vault-sync
description: Mantém o sistema de memória em 4 camadas do /root/hermes-vault e sincroniza um espelho operacional para o vault Obsidian principal em /root/hermes-wiki.
version: 1.0.0
author: Hermes Agent
license: MIT
---

# Hermes Memory Vault Sync

Use esta skill quando precisar operar ou restaurar o sistema de memória em camadas do Toni.

## Objetivo

Manter duas coisas em ordem:
1. o vault operacional local em `/root/hermes-vault`
2. o espelho visível no Obsidian principal em `/root/hermes-wiki/outputs/hermes-memory-system`

## Fonte de verdade atual

- Vault operacional: `/root/hermes-vault`
- Vault principal do Obsidian: `/root/hermes-wiki`
- `OBSIDIAN_VAULT_PATH=/root/hermes-wiki`

## Estrutura relevante

### No vault operacional
- `/root/hermes-vault/MEMORY_CORE.md`
- `/root/hermes-vault/Agent-Shared/user-profile.md`
- `/root/hermes-vault/Agent-Shared/project-state.md`
- `/root/hermes-vault/Agent-Shared/decisions-log.md`
- `/root/hermes-vault/Agent-Hermes/working-context.md`
- `/root/hermes-vault/Agent-Hermes/mistakes.md`
- `/root/hermes-vault/Agent-Hermes/daily/YYYY-MM-DD.md`

### Scripts operacionais
- `/root/hermes-vault/Agent-Hermes/scripts/bootstrap_memory.py`
- `/root/hermes-vault/Agent-Hermes/scripts/bootstrap_memory.sh`
- `/root/hermes-vault/Agent-Hermes/scripts/sync_to_obsidian.py`
- `/root/hermes-vault/Agent-Hermes/scripts/sync_to_obsidian.sh`

### No vault principal
- `/root/hermes-wiki/wiki/HERMES/sistema-de-memoria-em-camadas.md`
- `/root/hermes-wiki/outputs/hermes-memory-system/manifest.json`

## Fluxo padrão

### 1. Ler contexto local consolidado
Use:

```bash
python3 /root/hermes-vault/Agent-Hermes/scripts/bootstrap_memory.py
```

Para formato estruturado:

```bash
python3 /root/hermes-vault/Agent-Hermes/scripts/bootstrap_memory.py --json
```

### 2. Atualizar os arquivos do vault operacional
Antes de concluir uma tarefa, manter atualizados:
- `working-context.md`
- `decisions-log.md`
- `mistakes.md` quando houver erro
- `daily/YYYY-MM-DD.md` com append do que foi feito

### 3. Sincronizar para o Obsidian principal
Use:

```bash
python3 /root/hermes-vault/Agent-Hermes/scripts/sync_to_obsidian.py
```

Isso copia os arquivos operacionais para:

```bash
/root/hermes-wiki/outputs/hermes-memory-system/
```

E gera:
- `README.md`
- `manifest.json`
- cópias dos arquivos centrais

### 4. Validar
Checar:
- se `manifest.json` foi regenerado
- se os bytes/sha256 mudaram quando esperado
- se o espelho contém os arquivos atualizados

## Automação instalada

- sincronização automática a cada 5 minutos
- log em `/tmp/hermes-memory-sync.log`

## Pitfalls

- Não assumir que existem `USER.md` e `MEMORY.md` dentro de `/root/hermes-vault`; na implantação real eles não existiam.
- Não misturar a estrutura operacional do `/root/hermes-vault` com a estrutura editorial do `/root/hermes-wiki`.
- Não editar `raw/` no vault principal.
- Sempre validar `OBSIDIAN_VAULT_PATH` antes de sincronizar se houver suspeita de mudança de vault.

## Recuperação rápida

Se quiser revalidar tudo do zero:

```bash
python3 /root/hermes-vault/Agent-Hermes/scripts/bootstrap_memory.py --json
python3 /root/hermes-vault/Agent-Hermes/scripts/sync_to_obsidian.py
```

## Resultado esperado

- O vault operacional continua separado e enxuto.
- O Obsidian principal recebe um espelho legível e versionável.
- O início de sessão pode reler o contexto local sem depender só da memória nativa.
