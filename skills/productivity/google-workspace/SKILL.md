---
name: google-workspace
description: Gmail, Calendar, Drive, Contacts, Sheets, and Docs integration via gws CLI (googleworkspace/cli). Uses OAuth2 with automatic token refresh via bridge script. Requires gws binary.
version: 2.0.0
author: Nous Research
license: MIT
required_credential_files:
  - path: google_token.json
    description: Google OAuth2 token (created by setup script)
  - path: google_client_secret.json
    description: Google OAuth2 client credentials (downloaded from Google Cloud Console)
metadata:
  hermes:
    tags: [Google, Gmail, Calendar, Drive, Sheets, Docs, Contacts, Email, OAuth, gws]
    homepage: https://github.com/NousResearch/hermes-agent
    related_skills: [himalaya]
---

# Google Workspace

Gmail, Calendar, Drive, Contacts, Sheets, and Docs — powered by `gws` (Google's official Rust CLI). The skill provides a backward-compatible Python wrapper that handles OAuth token refresh and delegates to `gws`.

## Architecture

```
google_api.py  →  gws_bridge.py  →  gws CLI
(argparse compat)  (token refresh)    (Google APIs)
```

- `setup.py` handles OAuth2 (headless-compatible, works on CLI/Telegram/Discord)
- `gws_bridge.py` refreshes the Hermes token and injects it into `gws` via `GOOGLE_WORKSPACE_CLI_TOKEN`
- `google_api.py` provides the same CLI interface as v1 but delegates to `gws`

## References

- `references/gmail-search-syntax.md` — Gmail search operators (is:unread, from:, newer_than:, etc.)

## Scripts

- `scripts/setup.py` — OAuth2 setup (run once to authorize)
- `scripts/gws_bridge.py` — Token refresh bridge to gws CLI
- `scripts/google_api.py` — Backward-compatible API wrapper (delegates to gws)

## Prerequisites

Install `gws`:

```bash
cargo install google-workspace-cli
# or via npm (recommended, downloads prebuilt binary):
npm install -g @googleworkspace/cli
# or via Homebrew:
brew install googleworkspace-cli
```

Verify: `gws --version`

## First-Time Setup

The setup is fully non-interactive — you drive it step by step so it works
on CLI, Telegram, Discord, or any platform.

Define a shorthand first:

```bash
HERMES_HOME="${HERMES_HOME:-$HOME/.hermes}"
GWORKSPACE_SKILL_DIR="$HERMES_HOME/skills/productivity/google-workspace"
PYTHON_BIN="${HERMES_PYTHON:-python3}"
if [ -x "$HERMES_HOME/hermes-agent/venv/bin/python" ]; then
  PYTHON_BIN="$HERMES_HOME/hermes-agent/venv/bin/python"
fi
GSETUP="$PYTHON_BIN $GWORKSPACE_SKILL_DIR/scripts/setup.py"
```

### Step 0: Check if already set up

```bash
$GSETUP --check
```

If it prints `AUTHENTICATED`, skip to Usage — setup is already done.

### Step 1: Triage — ask the user what they need

**Question 1: "What Google services do you need? Just email, or also
Calendar/Drive/Sheets/Docs?"**

- **Email only** → Use the `himalaya` skill instead — simpler setup.
- **Calendar, Drive, Sheets, Docs (or email + these)** → Continue below.

**Partial scopes**: Users can authorize only a subset of services. The setup
script accepts partial scopes and warns about missing ones.

**Question 2: "Does your Google account use Advanced Protection?"**

- **No / Not sure** → Normal setup.
- **Yes** → Workspace admin must add the OAuth client ID to allowed apps first.

### Step 2: Create OAuth credentials (one-time, ~5 minutes)

Tell the user:

> 1. Go to https://console.cloud.google.com/apis/credentials
> 2. Create a project (or use an existing one)
> 3. Enable the APIs you need (Gmail, Calendar, Drive, Sheets, Docs, People)
> 4. Credentials → Create Credentials → OAuth 2.0 Client ID → Desktop app
> 5. Download JSON and tell me the file path

```bash
$GSETUP --client-secret /path/to/client_secret.json
```

### Step 3: Get authorization URL

```bash
$GSETUP --auth-url
```

Send the URL to the user. After authorizing, they paste back the redirect URL or code.

### Step 4: Exchange the code

```bash
$GSETUP --auth-code "THE_URL_OR_CODE_THE_USER_PASTED"
```

### Step 5: Verify

```bash
$GSETUP --check
```

Should print `AUTHENTICATED`. Token refreshes automatically from now on.

## Usage

All commands go through the API script:

```bash
HERMES_HOME="${HERMES_HOME:-$HOME/.hermes}"
GWORKSPACE_SKILL_DIR="$HERMES_HOME/skills/productivity/google-workspace"
PYTHON_BIN="${HERMES_PYTHON:-python3}"
if [ -x "$HERMES_HOME/hermes-agent/venv/bin/python" ]; then
  PYTHON_BIN="$HERMES_HOME/hermes-agent/venv/bin/python"
fi
GAPI="$PYTHON_BIN $GWORKSPACE_SKILL_DIR/scripts/google_api.py"
```

### Gmail

```bash
$GAPI gmail search "is:unread" --max 10
$GAPI gmail get MESSAGE_ID
$GAPI gmail send --to user@example.com --subject "Hello" --body "Message text"
$GAPI gmail send --to user@example.com --subject "Report" --body "<h1>Q4</h1>" --html
$GAPI gmail reply MESSAGE_ID --body "Thanks, that works for me."
$GAPI gmail labels
$GAPI gmail modify MESSAGE_ID --add-labels LABEL_ID
```

### Calendar

```bash
$GAPI calendar list
$GAPI calendar create --summary "Standup" --start 2026-03-01T10:00:00+01:00 --end 2026-03-01T10:30:00+01:00
$GAPI calendar create --summary "Review" --start ... --end ... --attendees "alice@co.com,bob@co.com"
$GAPI calendar delete EVENT_ID
```

### Drive

```bash
$GAPI drive search "quarterly report" --max 10
$GAPI drive search "mimeType='application/pdf'" --raw-query --max 5
```

### Contacts

```bash
$GAPI contacts list --max 20
```

### Sheets

```bash
$GAPI sheets get SHEET_ID "Sheet1!A1:D10"
$GAPI sheets update SHEET_ID "Sheet1!A1:B2" --values '[["Name","Score"],["Alice","95"]]'
$GAPI sheets append SHEET_ID "Sheet1!A:C" --values '[["new","row","data"]]'
```

### Docs

```bash
$GAPI docs get DOC_ID
```

### Direct gws access (advanced)

For operations not covered by the wrapper, use `gws_bridge.py` directly:

```bash
GBRIDGE="$PYTHON_BIN $GWORKSPACE_SKILL_DIR/scripts/gws_bridge.py"
$GBRIDGE calendar +agenda --today --format table
$GBRIDGE gmail +triage --labels --format json
$GBRIDGE drive +upload ./report.pdf
$GBRIDGE sheets +read --spreadsheet SHEET_ID --range "Sheet1!A1:D10"
```

## Output Format

All commands return JSON via `gws --format json`. Key output shapes:

- **Gmail search/triage**: Array of message summaries (sender, subject, date, snippet)
- **Gmail get/read**: Message object with headers and body text
- **Gmail send/reply**: Confirmation with message ID
- **Calendar list/agenda**: Array of event objects (summary, start, end, location)
- **Calendar create**: Confirmation with event ID and htmlLink
- **Drive search**: Array of file objects (id, name, mimeType, webViewLink)
- **Sheets get/read**: 2D array of cell values
- **Docs get**: Full document JSON (use `body.content` for text extraction)
- **Contacts list**: Array of person objects with names, emails, phones

Parse output with `jq` or read JSON directly.

## Rules

1. **Never send email or create/delete events without confirming with the user first.**
2. **Check auth before first use** — run `setup.py --check`.
3. **Use the Gmail search syntax reference** for complex queries.
4. **Calendar times must include timezone** — ISO 8601 with offset or UTC.
5. **Respect rate limits** — avoid rapid-fire sequential API calls.

## Multi-account / institutional setup notes

### Multiple Google accounts on one host

The base setup stores credentials in profile-scoped default files:
- `~/.hermes/google_client_secret.json`
- `~/.hermes/google_token.json`
- `~/.hermes/google_oauth_pending.json`

If you need to keep **two different Google accounts** active without overwriting each other (e.g. a project Gmail account plus an institutional school account), use **separate files per account** for:
- client secret
- token
- pending OAuth state

Example naming:
- `~/.hermes/google_token_coimbrabot.json`
- `~/.hermes/google_token_escola.json`
- `~/.hermes/google_oauth_pending_escola.json`

Do not reuse the same token file for both accounts unless you intentionally want to replace the prior login.

### Classroom + Forms institutional accounts

For school/workspace accounts that need **Google Classroom** and **Google Forms**, the standard Gmail/Calendar/Drive scopes are not enough. Include explicit scopes for Classroom and Forms during OAuth.

Typical additional scopes:
- `https://www.googleapis.com/auth/classroom.courses`
- `https://www.googleapis.com/auth/classroom.coursework.me`
- `https://www.googleapis.com/auth/classroom.coursework.students`
- `https://www.googleapis.com/auth/classroom.rosters`
- `https://www.googleapis.com/auth/classroom.profile.emails`
- `https://www.googleapis.com/auth/classroom.profile.photos`
- `https://www.googleapis.com/auth/forms.body`
- `https://www.googleapis.com/auth/forms.responses.readonly`

### Important real-world failure mode

Even when OAuth consent succeeds and Drive scope is present, **Drive can still fail** with `accessNotConfigured` if the **Google Drive API is not enabled in that specific Google Cloud project**.

Symptom:
- Classroom works
- Forms works
- Drive calls return HTTP 403 mentioning `drive.googleapis.com` not enabled for the project

Fix:
- Open the Google Cloud Console for the OAuth project
- Enable **Google Drive API** explicitly
- Wait a few minutes for propagation
- Retry the Drive call

## Troubleshooting

| Problem | Fix |
|---------|-----|
| `NOT_AUTHENTICATED` | Run setup Steps 2-5 |
| `REFRESH_FAILED` | Token revoked — redo Steps 3-5 |
| `gws: command not found` | Install: `npm install -g @googleworkspace/cli` |
| `HttpError 403` | Missing scope — `$GSETUP --revoke` then redo Steps 3-5 |
| `HttpError 403: Access Not Configured` | Enable the specific Google API in Google Cloud Console for the OAuth project |
| Advanced Protection blocks auth | Admin must allowlist the OAuth client ID |

### Multi-account pattern (important)

If you need to keep multiple Google accounts active (e.g. personal/project + school), do **not** reuse the default `google_token.json` / `google_client_secret.json` files for every account. Keep separate files per account, for example:

- `google_token_coimbrabot.json`
- `google_token_escola.json`
- `google_client_secret_coimbrabot.json`
- `google_client_secret_escola.json`
- `google_oauth_pending_coimbrabot.json`
- `google_oauth_pending_escola.json`

Why this matters:
- re-running the default setup overwrites the previous account's OAuth client + pending state
- a successful OAuth consent can still fail at runtime if the target API is not enabled in that specific Google Cloud project
- this showed up in practice with a school account where Classroom + Forms worked, but Drive returned `accessNotConfigured` until the Drive API was explicitly enabled for that OAuth project

Recommended workflow:
1. Keep one token/client-secret/pending trio per account
2. Label each trio by account or domain (`coimbrabot`, `escola`, etc.)
3. Decide the account from the resource owner before making API calls — e.g. Drive materials may live in a project account while Classroom/Forms live in a school account
4. After auth, test each required API separately (Gmail, Drive, Classroom, Forms)
5. If one API fails but others work, check API enablement in the Google Cloud project before redoing OAuth

### Inspecting Classroom / Forms links from URLs

When a browser link is login-gated, prefer the API with the already-authenticated account instead of trying to scrape the UI.

Useful patterns:
- Classroom URLs often embed base64-encoded numeric IDs. Example segments like `c/Nzkz...` and `a/ODE5...` decode to the numeric `courseId` and `courseWorkId` used by the Classroom API.
- The Forms ID is the `/d/<FORM_ID>/` segment and can be fetched directly with the Forms API.
- A Drive file ID from a shared URL returning `404 notFound` under one account usually means wrong account / missing sharing, not a bad parser.

Practical order:
1. Identify which Google account owns the resource.
2. Extract `courseId`, `courseWorkId`, `formId`, or `fileId` from the URL.
3. Query the matching API directly.
4. Only fall back to browser inspection when the API cannot answer the question.

## Revoking Access


The default setup script is single-profile and stores only one pair of files in `~/.hermes/`:
- `google_client_secret.json`
- `google_token.json`

If you need multiple Google accounts with different OAuth projects or different scope sets (e.g. personal Gmail vs school Classroom/Forms), do **not** overwrite the same token blindly. Use separate files per account/project, for example:
- `google_token_coimbrabot.json`
- `google_token_escola.json`
- `google_client_secret_escola.json`

Recommended pattern:
1. Keep one token file per account/project.
2. Keep one pending OAuth session file per account/project.
3. If an account needs extra scopes (e.g. Classroom + Forms), generate the auth URL with exactly those scopes and save the resulting token separately.
4. Test each Google API independently after auth (Gmail, Drive, Classroom, Forms).

### Classroom / Forms / Drive project gotcha

A token may be valid and still fail on a specific API if that API is not enabled in the Google Cloud project behind the OAuth client.

Real example observed in practice:
- Classroom auth: OK
- Forms auth: OK
- Drive auth scope present: OK
- Drive API calls: fail with `accessNotConfigured`

Cause: the Drive API was not enabled in that OAuth project.

Rule: when a Google account authenticates successfully but a specific service returns `accessNotConfigured`, check the API enablement for that project before redoing OAuth.

## Revoking Access



```bash
$GSETUP --revoke
```
