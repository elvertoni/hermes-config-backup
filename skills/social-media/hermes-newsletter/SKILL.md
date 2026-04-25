---
name: hermes-newsletter
description: Pipeline completo para gerar newsletter diária de IA a partir de perfis do X/Twitter. Coleta via twscrape, síntese com LLM, HTML estático com design system ProfessorDash, deploy automático via cron.
version: 1.0.0
author: Hermes Agent
---

# Hermes Newsletter — Pipeline de newsletter automática

## Arquitetura

```
cron job (diário 06h BRT)
  │
  ├─ script: collect.py (twscrape) → coleta tweets 38 perfis → stdout JSON
  │
  └─ agente Hermes:
       1. Lê tweets coletados
       2. Sintetiza destaques (3-6), headline, ranking "Em Movimento"
       3. Salva synthesis.json
       4. Roda render.py → preenche template.html → gera index.html
       5. Atualiza historico.json (últimas 30 edições)
       6. Deploy (cp para /var/www/hermes/ se existir)
```

## Coleta — twscrape (NÃO xurl)

**twscrape** é scraping como usuário comum do X. Autentica com login/senha de contas normais — zero developer account, zero Client ID, zero OAuth.

**xurl** é a API oficial do X (paga, precisa de developer account). NÃO usar para newsletter — o Toni prefere twscrape.

### Setup twscrape (usuário faz manualmente)

```bash
pip install twscrape

# Criar accounts.txt com credenciais:
# Formato: login:password:email:email_password
echo "seu_login:senha:email:senha_email" > accounts.txt

python -m twscrape add_accounts accounts.txt
python -m twscrape login_all
```

Para múltiplas contas (contorna rate limit), várias linhas no accounts.txt.

### Uso no Python

```python
from twscrape import API
api = API(pool_size=5)

# Buscar usuário por handle
user = await api.user_by_login("handle")

# Buscar tweets (async generator)
async for tweet in api.user_tweets(user.id, limit=10):
    # tweet.date (datetime), tweet.rawContent, tweet.url,
    # tweet.retweetCount, tweet.likeCount, tweet.viewCount
    pass
```

## Arquivos do pipeline

| Arquivo | Função |
|---|---|
| `~/.hermes/scripts/hermes-newsletter-collect.py` | Wrapper para cron (script deve estar na raiz de scripts/) |
| `~/.hermes/scripts/hermes-newsletter/collect.py` | Coleta tweets via twscrape, salva JSON, imprime sumário |
| `~/.hermes/scripts/hermes-newsletter/template.html` | Template HTML (dark theme, Geist, paleta ProfessorDash) |
| `~/.hermes/scripts/hermes-newsletter/render.py` | Preenche template com synthesis.json → index.html + historico.json |
| `~/.hermes/cron/output/tweets.json` | Dados brutos da coleta (output do collect.py) |
| `~/.hermes/cron/output/synthesis.json` | JSON estruturado gerado pelo agente (destaques, headline) |
| `~/.hermes/cron/output/index.html` | Página final renderizada |
| `~/.hermes/cron/output/historico.json` | Últimas 30 edições |

## Template HTML — Design System

Herda tokens visuais do ProfessorDash (`aulas.tonicoimbra.com`):
- **Background:** `#0f1117` (dark)
- **Fontes:** Geist (corpo), Geist Mono (código) do Google Fonts
- **Acentos:** verde `#10b981`, violeta `#8b5cf6`, ciano `#06b6d4`, coral `#f87171`
- **Cards:** `rgba(23,25,32,0.92)`, borda 1px, border-radius 1rem, hover: translateY(-1px)
- **Grid:** auto-fill minmax(320px, 1fr) → 1 col mobile, 2 tablet, 3 desktop
- **Tags:** badges coloridos por categoria com opacidade 0.15 no bg

### Cores por categoria (tag CSS classes)

| Tag | Cor | Classe CSS | Border |
|---|---|---|---|
| modelo | `#3b82f6` (blue) | `tag-modelo` | `tag-modelo-border` |
| ferramenta | `#10b981` (green) | `tag-ferramenta` | `tag-ferramenta-border` |
| pesquisa | `#8b5cf6` (violet) | `tag-pesquisa` | `tag-pesquisa-border` |
| infra | `#f97316` (orange) | `tag-infra` | `tag-infra-border` |
| agente | `#06b6d4` (cyan) | `tag-agente` | `tag-agente-border` |
| negócio | `#fbbf24` (amber) | `tag-negocio` | `tag-negocio-border` |
| opinião | `#6b7280` (gray) | `tag-opiniao` | `tag-opiniao-border` |

## Cron job

### Criar (exemplo)

```
schedule: 0 11 * * *  (11:00 CEST = 06:00 BRT)
script: hermes-newsletter-collect.py
deliver: local
enabled_toolsets: [terminal, file]
```

### Timezone

O servidor roda em **Europe/Berlin (CEST, UTC+2)**. Converter:
- `06:00 BRT (UTC-3)` = `09:00 UTC` = `11:00 CEST`
- Verificar com `timedatectl` ou `date` antes de agendar.

### Script constraint

Scripts de cron DEVEM ficar em `~/.hermes/scripts/` diretamente (não em subpastas). Para scripts em subdiretórios, criar wrapper na raiz:

```python
# ~/.hermes/scripts/hermes-newsletter-collect.py
import sys
sys.path.insert(0, "/root/.hermes/scripts/hermes-newsletter")
import collect
collect.main()
```

## Synthesis JSON schema (o agente deve gerar)

```json
{
  "data": "DD/MM/AAAA",
  "headline": "Frase resumo do dia (até ~120 chars)",
  "destaques": [
    {
      "titulo": "Até 10 palavras",
      "resumo": "2-4 linhas em português. Usar \\n para quebras.",
      "handle": "@handle",
      "url": "https://x.com/handle/status/ID",
      "tag": "modelo"
    }
  ],
  "em_movimento": ["@handle1", "@handle2", "@handle3", "@handle4", "@handle5"]
}
```

## Deploy

HTML gerado em `~/.hermes/cron/output/index.html`. Se houver servidor web:
```bash
mkdir -p /var/www/hermes/
cp ~/.hermes/cron/output/index.html /var/www/hermes/
cp ~/.hermes/cron/output/historico.json /var/www/hermes/
```

Se não houver `/var/www/hermes/`, o deploy é skipped (arquivos ficam no output dir).

## Perfis monitorados

38 perfis hardcoded em `collect.py`. Para alterar, editar a lista `PROFILES` no script.

## Pitfalls

- **NÃO usar xurl**: o Toni prefere twscrape (scraping como usuário). xurl precisa de developer account paga.
- **Script path**: cron jobs só aceitam scripts na raiz de `~/.hermes/scripts/`. Usar wrapper para subdiretórios.
- **twscrape sem login**: se `login_all` não foi rodado, `user_by_login` retorna None.
- **Rate limit**: sem múltiplas contas no twscrape, 38 perfis podem exceder limite. Usar `pool_size=5` e semáforo de concorrência.
- **Template encoding**: usar `html.escape()` em todo conteúdo vindo do Twitter/X antes de injetar no HTML.
- **JSON newlines**: resumos com quebras de linha devem usar `\n` escapado, nunca quebra literal.
- **Summer time**: CEST muda para CET no inverno (UTC+1). Revisar schedule do cron na troca de horário.
