#!/usr/bin/env python3
"""
Hermes Newsletter — Coleta de tweets.

Lê a lista de perfis monitorados, busca os tweets das últimas 24h
via xurl (X API v2) e salva o resultado em JSON.

Uso:
    python collect.py                          # salva em tweets.json
    python collect.py --output /tmp/t.json     # output customizado
    python collect.py --dry-run                # só imprime, não salva
"""

import json
import os
import subprocess
import sys
import time
from datetime import datetime, timedelta, timezone
from pathlib import Path

# Configuração
PROFILES = [
    "songjunkr", "OpenAI", "ClaudeDevs", "huggingface",
    "NanoClaw_AI", "opencode", "shiri_shh", "brivael",
    "alibaba_cloud", "wangray", "openclaw", "Hostinger",
    "elonmusk", "cryptopunk7213", "theo", "AkitaOnRails",
    "BytePlusGlobal", "gmi_cloud", "nahcrof", "warpdotdev",
    "Lonely__MH", "odysseyml", "vllm_project", "karpathy",
    "Abmankendrick", "baseten", "Kimi_Moonshot", "ctatedev",
    "joshua_xu_", "cavalry__app", "QuiverAI", "HeyGen",
    "ollama", "Alibaba_Qwen", "makulas1913", "birdabo",
    "berryxia", "leftcurvedev_",
]

MAX_TWEETS_PER_USER = 10
MAX_RESULTS = 5  # API param per request
OUTPUT_DIR = Path(os.environ.get("HERMES_NEWSLETTER_DIR", Path.home() / ".hermes/cron/output"))
OUTPUT_FILE = OUTPUT_DIR / "tweets.json"

# 24h cutoff in UTC
CUTOFF = datetime.now(timezone.utc) - timedelta(hours=24)


def run_xurl(*args):
    """Run xurl command, return parsed JSON or None on failure."""
    try:
        result = subprocess.run(
            ["xurl", *args],
            capture_output=True,
            text=True,
            timeout=30,
        )
        if result.returncode != 0:
            print(f"  ⚠ xurl failed (exit {result.returncode}): {result.stderr[:200]}", file=sys.stderr)
            return None
        return json.loads(result.stdout)
    except json.JSONDecodeError as e:
        print(f"  ⚠ JSON parse error: {e}", file=sys.stderr)
        return None
    except subprocess.TimeoutExpired:
        print(f"  ⚠ timeout", file=sys.stderr)
        return None
    except Exception as e:
        print(f"  ⚠ error: {e}", file=sys.stderr)
        return None


def get_user_id(username):
    """Resolve username to user ID via X API."""
    data = run_xurl("/2/users/by/username", username)
    if data and "data" in data:
        return data["data"]["id"]
    return None


def get_user_tweets(user_id, max_results=MAX_RESULTS):
    """Fetch recent tweets for a user."""
    fields = "created_at,public_metrics,entities"
    data = run_xurl(
        "/2/users", user_id, "tweets",
        f"max_results={max_results}",
        f"tweet.fields={fields}",
        "exclude=retweets,replies",  # only original posts
    )
    if data and "data" in data:
        return data["data"]
    # Try with includes if direct key not found
    if data:
        print(f"  ⚠ unexpected response shape: {list(data.keys())}", file=sys.stderr)
        # Try to find tweets in nested structure
        if "includes" in data and "tweets" in data.get("includes", {}):
            return data["includes"]["tweets"]
    return []


def filter_recent(tweets):
    """Keep only tweets from the last 24h."""
    recent = []
    for t in tweets:
        created = t.get("created_at", "")
        if not created:
            continue
        try:
            dt = datetime.fromisoformat(created.replace("Z", "+00:00"))
            if dt > CUTOFF:
                recent.append(t)
        except (ValueError, TypeError):
            continue
    return recent


def collect_all(dry_run=False):
    """Collect tweets from all monitored profiles."""
    output = {
        "coletado_em": datetime.now(timezone.utc).isoformat(),
        "cutoff": CUTOFF.isoformat(),
        "total_perfis": len(PROFILES),
        "perfis_com_dados": 0,
        "perfis_com_erro": 0,
        "total_tweets": 0,
        "perfis": [],
    }

    for i, username in enumerate(PROFILES, 1):
        print(f"[{i}/{len(PROFILES)}] @{username} ...", end=" ", flush=True)
        user_id = get_user_id(username)

        if not user_id:
            print("❌ (user not found)")
            output["perfis_com_erro"] += 1
            output["perfis"].append({
                "handle": username,
                "error": "user_not_found",
                "tweets": [],
            })
            time.sleep(0.5)  # rate limit breathing room
            continue

        tweets_raw = get_user_tweets(user_id)
        tweets_recent = filter_recent(tweets_raw)

        status = "🟢" if tweets_recent else "⚪"
        print(f"{status} {len(tweets_recent)} tweets recentes")

        output["perfis_com_dados"] += 1
        output["total_tweets"] += len(tweets_recent)
        output["perfis"].append({
            "handle": username,
            "user_id": user_id,
            "tweets": tweets_recent,
        })

        time.sleep(0.3)  # be gentle to the API

    # Remove empty profiles for cleaner output
    output["perfis"] = [p for p in output["perfis"] if p["tweets"]]

    if dry_run:
        print(f"\n📊 Dry run — {output['total_tweets']} tweets de {output['perfis_com_dados']} perfis")
        return output

    # Save to file
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
    with open(OUTPUT_FILE, "w", encoding="utf-8") as f:
        json.dump(output, f, ensure_ascii=False, indent=2)

    print(f"\n✅ Salvo em {OUTPUT_FILE}")
    print(f"   {output['total_tweets']} tweets de {len(output['perfis'])} perfis com dados")
    return output


if __name__ == "__main__":
    dry_run = "--dry-run" in sys.argv

    # Parse custom output path
    output_path = None
    for i, arg in enumerate(sys.argv):
        if arg == "--output" and i + 1 < len(sys.argv):
            output_path = Path(sys.argv[i + 1])
            OUTPUT_FILE = output_path
            OUTPUT_DIR = output_path.parent

    result = collect_all(dry_run=dry_run)

    # Print JSON summary for cron job context injection
    if not dry_run:
        # Print compact summary for agent consumption
        summary = {
            "coletado_em": result["coletado_em"],
            "total_tweets": result["total_tweets"],
            "perfis_ativos": len(result["perfis"]),
            "perfis": [
                {
                    "handle": p["handle"],
                    "tweet_count": len(p["tweets"]),
                    "tweets": [
                        {
                            "id": t["id"],
                            "text": t["text"],
                            "created_at": t.get("created_at", ""),
                            "metrics": t.get("public_metrics", {}),
                        }
                        for t in p["tweets"]
                    ],
                }
                for p in result["perfis"]
            ],
        }
        print("\n--- COLLECTION_SUMMARY_JSON ---")
        print(json.dumps(summary, ensure_ascii=False))
