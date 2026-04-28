---
name: google-oauth-token-censorship
description: Pitfall guide for Google OAuth token handling in Hermes — token censorship in execute_code, correct PKCE flow, and Notion API quirks.
version: 1.0.0
---

# Google OAuth + Notion API Pitfalls

## 1. Token Censorship in execute_code (CRITICAL)

When using `execute_code` with `terminal()`, **Google OAuth access tokens are censored** — the stdout shows `***` instead of the real token value. This means:

- ❌ `json.loads(result["output"])["access_token"]` → gets censored garbage (13 chars like `ya29.a...0206`)
- ✅ Do OAuth token exchange directly in `terminal()` (bash), then write token to JSON file via Python file I/O (not through string variables)

**Correct pattern:**
```bash
# In terminal(): exchange code and save token directly
RESP=$(curl -s -X POST "https://oauth2.googleapis.com/token" ...)
ACCESS=$(echo $RESP | jq -r '.access_token')
# Use $ACCESS directly in subsequent curl calls — don't pass through Python strings
```

## 2. PKCE Flow for OAuth

- Generate `code_verifier` (opaque random string, max 128 chars)
- Compute `code_challenge = base64url(sha256(code_verifier))`
- Build auth URL with `code_challenge_method=S256&access_type=offline&prompt=consent`
- Exchange code with `code_verifier` (not code_challenge)
- Client secret must match the OAuth project that generated the client_id

## 3. Refresh Token Revocation

When a new OAuth authorization is done for the same `client_id` + user, Google **revokes the previous refresh_token**. Always save the NEW refresh_token after each authorization.

## 4. Notion API: Workspace Pages Cannot Be Archived

`PATCH /v1/pages/{id}` with `{"archived": true}` returns HTTP 400: "Archiving workspace level pages via API not supported." Only pages inside databases can be archived. User must delete manually in Notion UI.

## 5. Notion: Large JSON Parsing

Notion block responses with 100+ blocks often contain control characters that break Python `json.loads()`. Always pipe through `jq` first:

```bash
curl ... | jq '[.results[] | {id, type, text}]'  # then parse in Python
```
