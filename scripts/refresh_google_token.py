#!/usr/bin/env python3
"""Renova token Google OAuth usando refresh_token. Executar via cron ou antes de usar APIs."""
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
    
    print(f"✅ Token renovado ({len(new['access_token'])} chars)")
    return 0

if __name__ == "__main__":
    sys.exit(refresh())
