---
name: hermes-newsletter
description: Pipeline completo para gerar newsletter diária de IA a partir de perfis do X/Twitter. Coleta via httpx + X GraphQL guest token, síntese com LLM, HTML estático com design system ProfessorDash, deploy automático via cron.
version: 1.1.0
author: Hermes Agent
---

# Hermes Newsletter — Pipeline de newsletter automática

## Arquitetura

```
cron job (diário 06h BRT)
  │
  ├─ script: collect.py (httpx + X GraphQL guest token) → coleta tweets 38 perfis → stdout JSON
  │
  └─ agente Hermes:
       1. Lê tweets coletados
       2. Sintetiza destaques (3-6), headline, ranking "Em Movimento"
       3. Salva synthesis.json
       4. Roda render.py → preenche template.html → gera index.html
       5. Atualiza historico.json (últimas 30 edições)
       6. Deploy: arquivos em cron/output/ → servidos por http.server:8082 → Cloudflare Tunnel
```

## Coleta — httpx + X GraphQL guest token (NÃO twscrape, NÃO xurl)

**Abordagem atual**: `collect.py` usa `httpx.Client` com User-Agent de browser + guest token da API pública do X para acessar os endpoints GraphQL. Zero dependência de login, developer account ou credenciais — funciona direto do IP da VPS.

**Histórico**: twscrape e curl_cffi foram bloqueados por fingerprint TLS (Cloudflare 1010) nesta VPS. A migração para httpx + guest token resolveu o problema.

**xurl** é a API oficial do X (paga, precisa de developer account). NÃO usar.

### Como funciona

```python
# O collect.py já está implementado — não reescrever
# Ele usa:
# 1. POST https://api.x.com/1.1/guest/activate.json → guest_token
# 2. GET https://x.com/i/api/graphql/{op} com Bearer token público
# 3. User-Agent de Chrome desktop
# 4. 0.5s delay entre perfis (rate limit)
```

### Cutoff dinâmico para dias de baixa atividade

O script usa `CUTOFF = timedelta(hours=24)` por padrão. Em **fins de semana e feriados** (quando < ~5 tweets em 24h), estender temporariamente para 72h e restaurar após a coleta:

```python
# Em collect.py, linha ~87:
CUTOFF = datetime.now(timezone.utc) - timedelta(hours=24)
# Para fins de semana, alterar para: timedelta(hours=72)
# Restaurar para 24h após a coleta
```

## Arquivos do pipeline

| Arquivo | Função |
|---|---|
| `~/.hermes/scripts/hermes-newsletter-collect.py` | Wrapper para cron (script deve estar na raiz de scripts/) |
| `~/.hermes/scripts/hermes-newsletter/collect.py` | Coleta tweets via httpx + X GraphQL guest token, salva JSON, imprime sumário |
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

Arquivos gerados em `~/.hermes/cron/output/`. O site é servido por Python http.server (porta 8082, bind 127.0.0.1) exposto via **Cloudflare Tunnel** no domínio `newsletter.tonicoimbra.com`.

```bash
# O servidor HTTP roda como processo background:
python3 -m http.server 8082 --bind 127.0.0.1

# Para atualizar o site live, editar diretamente o index.html:
patch ~/.hermes/cron/output/index.html ...
# Ou reposicionar os arquivos do output:
cp ~/.hermes/cron/output/index.html ~/.hermes/cron/output/historico.json /caminho/servido/
```

**NÃO existe `/var/www/hermes/`** — a seção de deploy anterior era hipotética. O deploy real é: arquivos em `cron/output/` → servidos pelo http.server → Cloudflare Tunnel → domínio público.

### Repositórios

| Repo | Local | Propósito |
|---|---|---|
| `elvertoni/newsletter` | `~/.hermes/scripts/hermes-newsletter/` | Código fonte (template, render.py, collect.py) |
| `elvertoni/hermes-config-backup` | `~/.hermes/hermes-config-backup/scripts/hermes-newsletter/` | Backup sanitizado do template |

O template **primário** usado pelo pipeline é o de `~/.hermes/scripts/hermes-newsletter/template.html`. O do config-backup é espelho — manter ambos sincronizados.

## Perfis monitorados

38 perfis hardcoded em `collect.py`. Para alterar, editar a lista `PROFILES` no script.

## Pitfalls

- **NÃO usar xurl**: API oficial paga, precisa de developer account.
- **NÃO usar twscrape**: bloqueado por fingerprint TLS (Cloudflare 1010) nesta VPS. O `collect.py` já usa httpx + guest token — manter essa abordagem.
- **NÃO reescrever collect.py**: ele já está funcional com httpx. Apenas editar a lista `PROFILES` ou o `CUTOFF` quando necessário.
- **Script path**: cron jobs só aceitam scripts na raiz de `~/.hermes/scripts/`. Usar wrapper para subdiretórios.
- **Cutoff de fim de semana**: domingos e feriados têm baixa atividade. Se < ~5 tweets em 24h, estender `CUTOFF` para 72h temporariamente e restaurar após coleta.
- **Template encoding**: usar `html.escape()` em todo conteúdo vindo do Twitter/X antes de injetar no HTML.
- **JSON newlines**: resumos com quebras de linha devem usar `\\n` escapado, nunca quebra literal.
- **Summer time**: CEST muda para CET no inverno (UTC+1). Revisar schedule do cron na troca de horário.
- **Síntese com poucos tweets**: quando há poucos tweets relevantes, priorizar os de maior engajamento (likes/RTs) e agrupar tweets relacionados ao mesmo tema em um único destaque.
