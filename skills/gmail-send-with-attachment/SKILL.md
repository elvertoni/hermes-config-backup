---
name: gmail-send-with-attachment
description: Send emails with attachments via Gmail API using the existing OAuth tokens on the system. Use when himalaya or gogcli aren't available, or when the user asks to send an email from coimbrabot.ai@gmail.com.
version: 1.0.0
author: hermes
metadata:
  hermes:
    tags: [Email, Gmail, Google, Drive, Attachments]
---

# Gmail Send with Attachment (via API)

Use this skill to send emails with attachments via Gmail API, using the existing OAuth tokens already configured on the system.

## When to use
- User asks to send an email (especially with attachments like PDF, DOCX, ZIP)
- himalaya is not installed or not configured
- gogcli is not available
- The sender is coimbrabot.ai@gmail.com

## Prerequisites
- Token file at `/root/.hermes/google_token.json` — OAuth token for coimbrabot.ai@gmail.com with `gmail.send` scope
- Python packages in the hermes-agent venv: `google-api-python-client`, `google-auth`, `google-auth-oauthlib`
- The venv is at `/root/.hermes/hermes-agent/venv/bin/python3`

## Token accounts available

| Token file | Account | Scopes | Use for |
|---|---|---|---|
| `/root/.hermes/google_token.json` | coimbrabot.ai@gmail.com | gmail.send, gmail.readonly, drive.readonly, calendar, contacts | Sending emails, Drive access |
| `/root/.hermes/google_token_escola.json` | Elvertoni.coimbra@escola.pr.gov.br | classroom.*, forms.*, drive, gmail | Classroom, Forms |

## Sending email with attachment

```python
import json, base64
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.base import MIMEBase
from email import encoders
from google.oauth2.credentials import Credentials
from googleapiclient.discovery import build

with open("/root/.hermes/google_token.json") as f:
    token_data = json.load(f)

creds = Credentials(
    token=token_data["token"],
    refresh_token=token_data["refresh_token"],
    token_uri=token_data["token_uri"],
    client_id=token_data["client_id"],
    client_secret=token_data["client_secret"],
    scopes=token_data["scopes"],
)

service = build("gmail", "v1", credentials=creds)

msg = MIMEMultipart()
msg["From"] = "coimbrabot.ai@gmail.com"
msg["To"] = "recipient@example.com"
msg["Subject"] = "Subject here"

body = "Plain text body here."
msg.attach(MIMEText(body, "plain", "utf-8"))

# Attach file
with open("/path/to/file.zip", "rb") as f:
    attachment = MIMEBase("application", "zip")
    attachment.set_payload(f.read())
encoders.encode_base64(attachment)
attachment.add_header("Content-Disposition", "attachment", filename="file.zip")
msg.attach(attachment)

raw = base64.urlsafe_b64encode(msg.as_bytes()).decode()
result = service.users().messages().send(userId="me", body={"raw": raw}).execute()
print(f"Email sent! ID: {result['id']}")
```

## Downloading files from Google Drive

```python
import json
from google.oauth2.credentials import Credentials
from googleapiclient.discovery import build
from googleapiclient.http import MediaIoBaseDownload

# Use same token loading pattern as above
service = build("drive", "v3", credentials=creds)

file_id = "GOOGLE_DRIVE_FILE_ID"
meta = service.files().get(fileId=file_id, fields="name,mimeType,size").execute()
print(f"File: {meta['name']} ({meta['mimeType']}, {meta.get('size', 'unknown')} bytes)")

output_path = f"/tmp/{meta['name']}"
request = service.files().get_media(fileId=file_id)
with open(output_path, "wb") as f:
    downloader = MediaIoBaseDownload(f, request)
    done = False
    while not done:
        status, done = downloader.next_chunk()
```

## MIME types for common attachments
- `.zip` → `application/zip`
- `.pdf` → `application/pdf`
- `.docx` → `application/vnd.openxmlformats-officedocument.wordprocessingml.document`
- `.pptx` → `application/vnd.openxmlformats-officedocument.presentationml.presentation`
- `.xlsx` → `application/vnd.openxmlformats-officedocument.spreadsheetml.sheet`
- `.png` → `image/png`
- `.jpg` → `image/jpeg`

## Pitfalls
- Token may expire; the refresh_token will auto-renew on next API call via google-auth library
- gdown does NOT work for files that aren't public — use Drive API instead
- himalaya needs manual OAuth config; the Drive API approach skips that entirely
- Always use `execute_code` tool for this (runs in the hermes-agent venv)
