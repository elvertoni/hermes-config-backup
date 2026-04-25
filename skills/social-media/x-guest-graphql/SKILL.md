---
name: x-guest-graphql
description: Acessa tweets públicos do X/Twitter via API GraphQL com guest token (sem login, sem developer account). Use quando twscrape ou curl_cffi falharem com bloqueio Cloudflare na VPS.
version: 1.0.0
---

# X Guest GraphQL API

Acesso anônimo (guest) à API GraphQL do X usando `httpx` simples com User-Agent de browser. Funciona em VPS onde `twscrape` e `curl_cffi` são bloqueados pelo Cloudflare por fingerprint TLS — a causa NÃO é bloqueio de IP.

## Pré-requisitos

```bash
pip install httpx
```

Zero credenciais. Zero developer account. Zero custo.

## Funcionamento

### 1. Obter guest token

```python
import httpx

headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/131.0.0.0 Safari/537.36",
    "Authorization": "Bearer AAAAAAAAAAAAAAAAAAAAANRILgAAAAAAnNwIzUejRCOuH5E6I8xnZz4puTs=1Zv7ttfk8LF81IUq16cHjhLTvJu4FA33AGWWjCpTnA",
}
resp = httpx.post("https://api.x.com/1.1/guest/activate.json", headers=headers)
guest_token = resp.json()["guest_token"]
headers["X-Guest-Token"] = guest_token
```

O Bearer token é público — vem do client web do X.

### 2. Resolver @handle → user ID

Query ID: `32pL5BWe9WKeSK1MoPvFQQ/UserByScreenName`

```python
import json

variables = {"screen_name": "karpathy"}
features = json.dumps({"hidden_profile_subscriptions_enabled": True, ...})  # ver features completas abaixo

resp = httpx.get(
    "https://x.com/i/api/graphql/32pL5BWe9WKeSK1MoPvFQQ/UserByScreenName",
    params={"variables": json.dumps(variables), "features": features},
    headers=headers,
)
user_id = resp.json()["data"]["user"]["result"]["rest_id"]
```

### 3. Buscar tweets do usuário

Query ID: `HeWHY26ItCfUmm1e6ITjeA/UserTweets`

```python
variables = {
    "userId": user_id,
    "count": 10,
    "includePromotedContent": False,
    "withQuickPromoteEligibilityTweetFields": False,
    "withVoice": False,
    "withV2Timeline": True,
}

resp = httpx.get(
    "https://x.com/i/api/graphql/HeWHY26ItCfUmm1e6ITjeA/UserTweets",
    params={"variables": json.dumps(variables), "features": features},
    headers=headers,
)
data = resp.json()

# Estrutura da resposta:
# data.user.result.timeline.timeline.instructions[]
#   → type: "TimelineAddEntries"
#     → entries[].content.itemContent.tweet_results.result
#       → __typename: "Tweet"
#         → legacy.full_text, legacy.created_at, legacy.favorite_count, etc.
```

### 4. Features payload completo

```python
FEATURES = json.dumps({
    "rweb_tipjar_consumption_enabled": True,
    "responsive_web_graphql_exclude_directive_enabled": True,
    "verified_phone_label_enabled": False,
    "creator_subscriptions_tweet_preview_api_enabled": True,
    "responsive_web_graphql_timeline_navigation_enabled": True,
    "responsive_web_graphql_skip_user_profile_image_extensions_enabled": False,
    "communities_web_enable_tweet_community_results_fetch": True,
    "c9s_tweet_anatomy_moderator_badge_enabled": True,
    "articles_preview_enabled": True,
    "responsive_web_edit_tweet_api_enabled": True,
    "graphql_is_translatable_rweb_tweet_is_translatable_enabled": True,
    "view_counts_everywhere_api_enabled": True,
    "longform_notetweets_consumption_enabled": True,
    "responsive_web_twitter_article_tweet_consumption_enabled": True,
    "tweet_awards_web_tipping_enabled": False,
    "creator_subscriptions_quote_tweet_preview_enabled": False,
    "freedom_of_speech_not_reach_fetch_enabled": True,
    "standardized_nudges_misinfo": True,
    "tweet_with_visibility_results_prefer_gql_limited_actions_policy_enabled": True,
    "rweb_video_timestamps_enabled": True,
    "longform_notetweets_rich_text_read_enabled": True,
    "longform_notetweets_inline_media_enabled": True,
    "responsive_web_enhance_cards_enabled": False,
})
```

## Estrutura da resposta de tweets

Cada tweet extraído tem estes campos:

```python
{
    "id": str,             # legacy.id_str
    "url": str,            # https://x.com/i/web/status/{id}
    "text": str,           # legacy.full_text
    "created_at": str,     # "Fri Apr 24 16:57:55 +0000 2026"
    "retweet_count": int,  # legacy.retweet_count
    "favorite_count": int, # legacy.favorite_count
    "reply_count": int,    # legacy.reply_count
    "quote_count": int,    # legacy.quote_count
    "view_count": int,     # legacy.views.count
    "lang": str,           # legacy.lang
}
```

## Rate limiting

- Guest tokens têm rate limit ~50-100 requests por token
- Usar `time.sleep(0.5)` entre perfis para evitar bloqueio
- Guest token expira — renovar se começar a falhar

## Pitfalls

- **Query IDs mudam**: o X atualiza os query IDs periodicamente. Se começar a dar 404 "Query not found", os IDs precisam ser atualizados (extrair do source do x.com ou de projetos como twscrape).
- **twscrape NÃO funciona nesta VPS**: o bloqueio é no fingerprint TLS do `httpx.AsyncClient` com as configs específicas do twscrape (headers customizados, x-client-transaction-id), não no IP.
- **curl_cffi também falha**: Cloudflare bloqueia `curl_cffi` nos endpoints de API (/i/api/graphql e /1.1/guest/activate.json), mesmo com impersonate=chrome120.
- **httpx simples FUNCIONA**: usar `httpx.Client` (não `AsyncClient`) com o User-Agent de browser listado acima.
- **RTs**: tweets começando com "RT @" devem ser filtrados.
- **Timezone**: `created_at` vem em UTC (`+0000`). Formato: `"%a %b %d %H:%M:%S %z %Y"` (ex: `"Fri Apr 24 16:57:55 +0000 2026"`). Converter para BRT subtraindo 3h se necessário.
- **Query IDs**: `UserByScreenName` = `32pL5BWe9WKeSK1MoPvFQQ` (NÃO usar `1VOOyvKkiI3FMmKeDNxM9A` — twscrape desatualizado, retorna 404). `UserTweets` = `HeWHY26ItCfUmm1e6ITjeA`. Para encontrar IDs novos: `grep -n "OP_" twscrape/api.py`.
- **URL de tweet**: usar `https://x.com/i/web/status/{id}` (formato canônico web). Evitar `/i/status/{id}` (redireciona).
- **Teste prévio**: `curl -s -o /dev/null -w "%{http_code}" -H "User-Agent: ...Chrome/131..." https://x.com` → 200 = OK, 403 = IP bloqueado.

## Cloudflare Tunnel com newsletter

Se o túnel for **remotely-managed** (config no dashboard Cloudflare), o YAML local é ignorado para as regras de ingress. Apenas `tunnel` e `credentials-file` são usados. As rotas devem ser adicionadas via **Zero Trust → Networks → Tunnels → Public Hostname**. O comando `cloudflared tunnel route dns` cria um CNAME que conflita com o dashboard — se já existir, delete o registro DNS antes de adicionar pelo dashboard.

## Implementação de referência

Script completo em `~/.hermes/scripts/hermes-newsletter/collect.py` — coleta de 38 perfis com filtro de 24h e exclusão de RTs.
