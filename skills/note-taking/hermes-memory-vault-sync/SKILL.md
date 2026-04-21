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
2. o espelho Git/publicável em `/root/hermes-wiki`

## Fonte de verdade atual

- Vault operacional: `/root/hermes-vault`
- Obsidian no Windows: aponta para o vault operacional sincronizado por Syncthing
- Espelho Git/publicável: `/root/hermes-wiki`
- Backup sanitizado de skills/config: `/root/hermes-config-backup`

## Topologia real atual

- `/root/hermes-vault` = fonte operacional principal
- Dell G15 (`TONI_G15`) = sincroniza bidirecionalmente `/root/hermes-vault` via Syncthing
- Syncthing no Windows roda como serviço via NSSM
- `/root/hermes-wiki` = espelho Git para consulta/publicação
- `/root/.hermes` = runtime local de skills/config

## Estrutura relevante

### No vault operacional
- `/root/hermes-vault/MEMORY_CORE.md`
- `/root/hermes-vault/Agent-Shared/user-profile.md`
- `/root/hermes-vault/Agent-Shared/project-state.md`
- `/root/hermes-vault/Agent-Shared/decisions-log.md`
- `/root/hermes-vault/Agent-Hermes/working-context.md`
- `/root/hermes-vault/Agent-Hermes/mistakes.md`
- `/root/hermes-vault/Agent-Hermes/RESSURREICAO.md`
- `/root/hermes-vault/Agent-Hermes/daily/YYYY-MM-DD.md`
- `/root/hermes-vault/Agent-Hermes/skills/coimbraclaw-prof.md`
- `/root/hermes-vault/Agent-Hermes/skills/coimbraclaw-revisao.md`
- `/root/hermes-vault/Agent-Hermes/skills/coimbraclaw-estatica.md`
- `/root/hermes-vault/raw/{inbox,pessoal,referencias,professor,dev,hermes,assets}`
- `/root/hermes-vault/wiki/{HERMES,PROFESSOR,DEV,PESSOAL,REFERENCIAS,sintese}`

### Scripts operacionais
- `/root/hermes-vault/Agent-Hermes/scripts/bootstrap_memory.py`
- `/root/hermes-vault/Agent-Hermes/scripts/bootstrap_memory.sh`
- `/root/hermes-vault/Agent-Hermes/scripts/sync_to_obsidian.py`
- `/root/hermes-vault/Agent-Hermes/scripts/sync_to_obsidian.sh`

### No espelho Git
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

### 3. Sincronizar para o espelho Git / Obsidian publicado
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
- export de `RESSURREICAO.md`
- cópias das skills locais do professor quando previstas pelo script

### 4. Validar
Checar:
- se `manifest.json` foi regenerado
- se os bytes/sha256 mudaram quando esperado
- se o espelho contém os arquivos atualizados
- se `RESSURREICAO.md` apareceu no espelho quando alterado
- se o conteúdo crítico também chegou ao vault do Windows via Syncthing

## Automação instalada

- sincronização automática local a cada 5 minutos para o espelho Git
- log em `/tmp/hermes-memory-sync.log`
- Syncthing mantendo `/root/hermes-vault` em tempo real com o Dell G15 (`TONI_G15`)
- Syncthing no Windows configurado como serviço via NSSM

## Pitfalls

- Não assumir que existem `USER.md` e `MEMORY.md` dentro de `/root/hermes-vault`; na implantação real eles não existiam.
- Não tratar `/root/hermes-wiki` como fonte operacional principal quando o fluxo ativo estiver usando Syncthing + Obsidian no Windows; hoje ele é espelho Git/publicável.
- Não misturar a estrutura operacional do `/root/hermes-vault` com a estrutura editorial do `/root/hermes-wiki`.
- Não esquecer de sincronizar snapshots em `Agent-Hermes/skills/` quando as 3 skills do professor mudarem de forma estrutural.
- Não editar `raw/` no vault principal.
- Sempre validar o sentido do sync: Syncthing cuida de `/root/hermes-vault`; `sync_to_obsidian.py` cuida do espelho em `/root/hermes-wiki`.

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
