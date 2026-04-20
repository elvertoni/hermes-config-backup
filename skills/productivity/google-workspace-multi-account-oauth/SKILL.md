---
name: google-workspace-multi-account-oauth
description: Configurar múltiplas contas Google com OAuth em paralelo, usando tokens separados por conta e validando Gmail/Drive/Classroom/Forms individualmente. Use quando uma conta não pode sobrescrever a outra ou quando o projeto OAuth tem APIs habilitadas de forma diferente.
version: 1.0.0
author: Hermes Agent
license: MIT
---

# Google Workspace Multi-Account OAuth

Use esta skill quando precisar autenticar mais de uma conta Google no mesmo host sem sobrescrever o token padrão, especialmente em cenários como:

- uma conta pessoal/projeto (`coimbrabot.ai@gmail.com`)
- uma conta institucional (`@escola.pr.gov.br`)
- escopos diferentes por conta (ex.: Gmail/Drive numa, Classroom/Forms noutra)

## Quando usar

- o setup padrão grava tudo em `~/.hermes/google_token.json` e você precisa manter outra conta em paralelo
- a conta institucional precisa de `Forms` e `Classroom`
- você precisa diagnosticar se a falha é OAuth, escopo ou API desabilitada no projeto do Google Cloud

## Princípio

Não sobrescreva o token da conta já funcional.

Use arquivos separados por conta:
- `google_client_secret_<conta>.json`
- `google_token_<conta>.json`
- `google_oauth_pending_<conta>.json`

## Abordagem

### Conta 1 — conta já suportada pelo setup padrão

Se a conta puder usar o fluxo padrão da skill `google-workspace`, siga o setup normal:

```bash
python3 ~/.hermes/skills/productivity/google-workspace/scripts/setup.py --client-secret /caminho/client_secret.json
python3 ~/.hermes/skills/productivity/google-workspace/scripts/setup.py --auth-url
# usuário autoriza e devolve a URL/código
python3 ~/.hermes/skills/productivity/google-workspace/scripts/setup.py --auth-code 'URL_OU_CODE'
python3 ~/.hermes/skills/productivity/google-workspace/scripts/setup.py --check
```

### Conta 2+ — fluxo paralelo sem sobrescrever token existente

Quando precisar manter outra conta em paralelo, use um helper com token/callback separados.

#### 1. Salvar o client secret da nova conta

Exemplo:

```bash
cat > /root/google-client-secret-escola.json
```

#### 2. Criar helper OAuth separado

Crie um script simples que:
- receba `--client-secret`
- receba `--token`
- receba `--pending`
- gere `--auth-url`
- troque `--auth-code`
- use escopos específicos por perfil

Escopos úteis para conta escolar com Classroom + Forms:

```python
[
  'https://www.googleapis.com/auth/classroom.courses',
  'https://www.googleapis.com/auth/classroom.coursework.me',
  'https://www.googleapis.com/auth/classroom.coursework.students',
  'https://www.googleapis.com/auth/classroom.rosters',
  'https://www.googleapis.com/auth/classroom.profile.emails',
  'https://www.googleapis.com/auth/classroom.profile.photos',
  'https://www.googleapis.com/auth/forms.body',
  'https://www.googleapis.com/auth/forms.responses.readonly',
  'https://www.googleapis.com/auth/drive',
  'https://www.googleapis.com/auth/gmail.readonly',
  'https://www.googleapis.com/auth/gmail.send',
  'https://www.googleapis.com/auth/gmail.modify',
  'https://www.googleapis.com/auth/calendar',
]
```

#### 3. Gerar a URL de autorização

```bash
python3 /root/google_oauth_account.py \
  --profile school \
  --client-secret /root/google-client-secret-escola.json \
  --token /root/.hermes/google_token_escola.json \
  --pending /root/.hermes/google_oauth_pending_escola.json \
  --auth-url
```

#### 4. Usuário autoriza e devolve a URL completa

Aceite a URL inteira retornada em `http://localhost:1/?state=...&code=...&scope=...`

#### 5. Trocar o código pelo token

```bash
python3 /root/google_oauth_account.py \
  --profile school \
  --client-secret /root/google-client-secret-escola.json \
  --token /root/.hermes/google_token_escola.json \
  --pending /root/.hermes/google_oauth_pending_escola.json \
  --auth-code 'URL_COMPLETA_DE_CALLBACK'
```

#### 6. Validar o token salvo

```bash
python3 /root/google_oauth_account.py \
  --profile school \
  --client-secret /root/google-client-secret-escola.json \
  --token /root/.hermes/google_token_escola.json \
  --pending /root/.hermes/google_oauth_pending_escola.json \
  --check
```

## Validação real por API

Depois da autenticação, teste cada serviço separadamente.

### Classroom

Use `googleapiclient.discovery.build('classroom', 'v1', credentials=creds)` e rode algo como:

```python
svc.courses().list(pageSize=5).execute()
```

### Forms

Teste criação de um formulário simples:

```python
svc = build('forms', 'v1', credentials=creds, cache_discovery=False)
svc.forms().create(body={'info': {'title': 'Hermes test form'}}).execute()
```

### Drive

Teste listagem simples:

```python
svc = build('drive', 'v3', credentials=creds, cache_discovery=False)
svc.files().list(pageSize=5, fields='files(id,name,mimeType)').execute()
```

## Diagnóstico importante

Se `Classroom` e `Forms` funcionarem mas `Drive` falhar com erro 403 `accessNotConfigured`, o motivo real normalmente é:

- a conta foi autenticada com escopo de Drive
- MAS a Drive API não está habilitada no projeto OAuth do Google Cloud

Mensagem típica:
- `Google Drive API has not been used in project ... before or it is disabled`

### Correção

Abrir o link de enable da API e ativar:

```text
https://console.developers.google.com/apis/api/drive.googleapis.com/overview?project=<PROJECT_ID>
```

Depois esperar alguns minutos e testar novamente.

## Regra prática de operação

- `coimbrabot.ai@gmail.com`: pode usar token padrão se isso simplificar
- conta institucional: preferir token separado se tiver escopos/API diferentes
- sempre testar os serviços reais após OAuth; não assumir que escopo concedido implica API habilitada

## Pitfalls

1. Não reutilizar o mesmo `google_token.json` para contas diferentes.
2. Não assumir que autorização com escopo de Drive significa Drive operacional.
3. Não misturar callback pendente entre contas (`google_oauth_pending*.json`).
4. Não validar só com `--check`; testar as APIs reais (Classroom/Forms/Drive/Gmail).
5. Em conta institucional, esperar mais chance de bloqueio por admin ou API desabilitada.

## Resultado esperado

Ao final, você terá múltiplas contas funcionais no mesmo host, com tokens separados e validação real por serviço, sem sobrescrever a conta anterior.
