# Hermes Config Backup

Backup sanitizado do diretório `/root/.hermes`.

Repositório:
- GitHub: `https://github.com/elvertoni/hermes-config-backup`
- Tipo: privado

## Objetivo

Preservar o que é estrutural e reutilizável no Hermes sem subir segredos, credenciais ou estados efêmeros.

Este repositório existe para manter versionados:
- skills
- scripts operacionais
- configuração sanitizada

## O que entra no backup

### 1. Skills
Origem:
- `/root/.hermes/skills/`

Inclui:
- `SKILL.md`
- referências, templates, assets e scripts das skills
- skills criadas localmente, como:
  - `hermes-memory-vault-sync`
  - `hermes-github-backups`

### 2. Scripts operacionais
Origem:
- `/root/.hermes/scripts/`

Inclui, por exemplo:
- `obsidian-auto-push.sh`
- `hermes-config-backup.sh`
- `export-hermes-config-backup.py`

### 3. Configuração sanitizada
Origem real:
- `/root/.hermes/config.yaml`

Arquivo salvo no backup:
- `config/config.redacted.yaml`

Esse arquivo é gerado com redação de campos sensíveis.

## O que NÃO entra no backup

Excluído de propósito:
- `/root/.hermes/.env`
- `/root/.hermes/auth.json`
- `/root/.hermes/google_token.json`
- `/root/.hermes/google_token_escola.json`
- `/root/.hermes/google_client_secret.json`
- `/root/.hermes/sessions/`
- `/root/.hermes/logs/`
- `/root/.hermes/state.db`
- `/root/.hermes/state.db-shm`
- `/root/.hermes/state.db-wal`
- `/root/.hermes/gateway_state.json`
- `/root/.hermes/processes.json`
- caches, locks e outros estados efêmeros

## Motivo das exclusões

Esses arquivos não devem ir para o Git porque podem conter:
- tokens e credenciais reais
- histórico privado de conversa
- estado transitório do runtime
- dados locais que não fazem sentido como código/configuração

## Como a sanitização funciona

O export é feito por:
- `/root/.hermes/scripts/export-hermes-config-backup.py`

Ele:
- copia `skills/`
- copia `scripts/`
- lê `config.yaml`
- gera `config/config.redacted.yaml`
- substitui campos sensíveis por `REDACTED`

Exemplos de campos redigidos:
- `api_key`
- `token`
- `client_secret`
- `access_token`
- `refresh_token`
- strings que parecem chaves reais, como prefixos `sk-`, `ghp_` e `github_pat_`

## Automação

Script principal:
- `/root/.hermes/scripts/hermes-config-backup.sh`

Cron ativo:
- `*/5 * * * * /root/.hermes/scripts/hermes-config-backup.sh >> /tmp/hermes-config-backup.log 2>&1`

Log local:
- `/tmp/hermes-config-backup.log`

## Validação prática

Para reexecutar manualmente:

```bash
python3 /root/.hermes/scripts/export-hermes-config-backup.py
/root/.hermes/scripts/hermes-config-backup.sh
```

Para inspecionar o conteúdo redigido:

```bash
sed -n '1,120p' /root/hermes-config-backup/config/config.redacted.yaml
```

## Garantia prática deste repositório

Se uma skill, instrução ou script operacional for ajustado em `/root/.hermes`, ele entra neste backup Git.

Se uma configuração for sensível, ela só entra em forma sanitizada.

Ou seja:
- conhecimento operacional: sim
- segredos reais: não
