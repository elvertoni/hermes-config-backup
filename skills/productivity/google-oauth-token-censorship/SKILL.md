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

## 2. PKCE Flow for OAuth — Complete Bash Pattern

### One-Time: Get ALL scopes at once

Generate ONE auth URL with every scope you'll ever need. This avoids repeated re-authorizations that revoke previous refresh_tokens.

```bash
# 1. Generate PKCE params and auth URL (Python helper)
python3 << 'PYEOF'
import secrets, hashlib, base64, urllib.parse, json

CLIENT_ID = "YOUR_CLIENT_ID.apps.googleusercontent.com"
REDIRECT_URI = "http://localhost:1"
SCOPES = [
    "https://www.googleapis.com/auth/drive",
    "https://www.googleapis.com/auth/documents",
    "https://www.googleapis.com/auth/spreadsheets",
    "https://www.googleapis.com/auth/gmail.readonly",
    "https://www.googleapis.com/auth/gmail.send",
    "https://www.googleapis.com/auth/gmail.modify",
    "https://www.googleapis.com/auth/calendar",
    "https://www.googleapis.com/auth/contacts.readonly",
]

code_verifier = secrets.token_urlsafe(96)
code_challenge = base64.urlsafe_b64encode(
    hashlib.sha256(code_verifier.encode()).digest()
).rstrip(b'=').decode()
state = secrets.token_urlsafe(16)

params = {
    "response_type": "code",
    "client_id": CLIENT_ID,
    "redirect_uri": REDIRECT_URI,
    "scope": " ".join(SCOPES),
    "state": state,
    "code_challenge": code_challenge,
    "code_challenge_method": "S256",
    "access_type": "offline",
    "prompt": "consent",
}
auth_url = "https://accounts.google.com/o/oauth2/auth?" + urllib.parse.urlencode(params, quote_via=urllib.parse.quote)

# Save PKCE data for exchange step
with open("/tmp/oauth_pending.json", "w") as f:
    json.dump({"code_verifier": code_verifier, "state": state,
               "client_id": CLIENT_ID, "redirect_uri": REDIRECT_URI}, f)

print(auth_url)
PYEOF
```

### Exchange code → token (MUST be in raw terminal, NOT execute_code)

```bash
CODE="4/0AeoWuM..."  # from user's callback URL
CLIENT_ID="..."
CLIENT_SECRET="GOCSPX-..."  # from google_client_secret.json
CODE_VERIFIER=$(jq -r '.code_verifier' /tmp/oauth_pending.json)

# Exchange — do NOT use execute_code (token gets censored to ***)
RESP=$(curl -s -X POST "https://oauth2.googleapis.com/token" \
  -d "code=$CODE" \
  -d "client_id=$CLIENT_ID" \
  -d "client_secret=$CLIENT_SECRET" \
  -d "redirect_uri=http://localhost:1" \
  -d "code_verifier=$CODE_VERIFIER" \
  -d "grant_type=authorization_code")

ACCESS=$(echo "$RESP" | jq -r '.access_token')
REFRESH=$(echo "$RESP" | jq -r '.refresh_token')
SCOPE=$(echo "$RESP" | jq -r '.scope')

# Verify token works BEFORE saving
curl -s "https://www.googleapis.com/drive/v3/about?fields=user" \
  -H "Authorization: Bearer $ACCESS" | jq '{user: .user.emailAddress}'

# Save to token file via Python file I/O (safe)
python3 -c "
import json
with open('/root/.hermes/google_token.json') as f:
    d = json.load(f)
d['token'] = '$ACCESS'
d['refresh_token'] = '$REFRESH'
d['scopes'] = '$SCOPE'.split(' ')
with open('/root/.hermes/google_token.json', 'w') as f:
    json.dump(d, f, indent=2)
"
```

### Auto-refresh script (no user intervention ever again)

Save as `~/.hermes/scripts/refresh_google_token.py`:

```python
import json, urllib.request, os, sys
TOKEN_FILE = os.path.expanduser("~/.hermes/google_token.json")

def refresh():
    with open(TOKEN_FILE) as f:
        d = json.load(f)
    data = urllib.parse.urlencode({
        "client_id": d["client_id"],
        "client_secret": d["client_secret"],
        "refresh_token": d["refresh_token"],
        "grant_type": "refresh_token",
    }).encode()
    req = urllib.request.Request("https://oauth2.googleapis.com/token", data=data)
    with urllib.request.urlopen(req) as resp:
        new = json.loads(resp.read())
    d["token"] = new["access_token"]
    with open(TOKEN_FILE, "w") as f:
        json.dump(d, f, indent=2)
    return 0

if __name__ == "__main__":
    sys.exit(refresh())
```

Run before any Google API call: `python3 ~/.hermes/scripts/refresh_google_token.py`

## 3. Refresh Token Revocation

When a new OAuth authorization is done for the same `client_id` + user, Google **revokes the previous refresh_token**. Always save the NEW refresh_token after each authorization.

## 4. Notion API: Workspace Pages Cannot Be Archived

`PATCH /v1/pages/{id}` with `{"archived": true}` returns HTTP 400: "Archiving workspace level pages via API not supported." Only pages inside databases can be archived. User must delete manually in Notion UI.

## 5. Notion: Large JSON Parsing

Notion block responses with 100+ blocks often contain control characters that break Python `json.loads()`. Always pipe through `jq` first:

```bash
curl ... | jq '[.results[] | {id, type, text}]'  # then parse in Python
```

## 6. Google Drive Upload Patterns

### Upload DOCX → Google Doc (preserves template header/footer)

```bash
ACCESS=$(python3 -c "import json; print(json.load(open('/root/.hermes/google_token.json'))['token'])")
BOUNDARY="boundary123"
METADATA='{"name":"Document Name","mimeType":"application/vnd.google-apps.document"}'

(
  echo "--$BOUNDARY"
  echo "Content-Type: application/json; charset=UTF-8"
  echo ""
  echo "$METADATA"
  echo "--$BOUNDARY"
  echo "Content-Type: application/vnd.openxmlformats-officedocument.wordprocessingml.document"
  echo ""
  cat /tmp/document.docx
  echo ""
  echo "--$BOUNDARY--"
) > /tmp/multipart.txt

curl -s -X POST "https://www.googleapis.com/upload/drive/v3/files?uploadType=multipart" \
  -H "Authorization: Bearer $ACCESS" \
  -H "Content-Type: multipart/related; boundary=$BOUNDARY" \
  --data-binary @/tmp/multipart.txt | jq '{id, name}'
```

### Upload HTML → Google Doc

Same pattern, use `Content-Type: text/html` and `mimeType: application/vnd.google-apps.document`.

### Build DOCX with python-docx preserving header

```python
from docx import Document
doc = Document("template_with_header.docx")  # opens preserving header/footer/images
# Add body content...
doc.save("output.docx")
```
