#!/usr/bin/env python3
"""
Hermes Newsletter — Coleta de tweets via twscrape.

Usa twscrape (scraping como usuário comum do X) para buscar tweets
das últimas 24h dos perfis monitorados. Zero developer account.

Requer setup prévio:
    python -m twscrape add_accounts accounts.txt login:password:email:email_password
    python -m twscrape login_all

Uso:
    python collect.py                          # salva em tweets.json
    python collect.py --output /tmp/t.json     # output customizado
    python collect.py --dry-run                # só imprime, não salva
"""

import asyncio
import json
import os
import sys
from datetime import datetime, timedelta, timezone
from pathlib import Path

from twscrape import API

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

OUTPUT_DIR = Path(os.environ.get("HERMES_NEWSLETTER_DIR", Path.home() / ".hermes/cron/output"))
OUTPUT_FILE = OUTPUT_DIR / "tweets.json"
MAX_TWEETS_PER_USER = 10

# 24h cutoff in UTC (timezone-aware)
CUTOFF = datetime.now(timezone.utc) - timedelta(hours=24)


def tweet_to_dict(tweet) -> dict:
    """Convert twscrape Tweet object to a plain dict."""
    return {
        "id": tweet.id,
        "id_str": str(tweet.id),
        "url": tweet.url,
        "text": tweet.rawContent if hasattr(tweet, "rawContent") else tweet.text,
        "created_at": tweet.date.isoformat() if tweet.date else None,
        "retweet_count": getattr(tweet, "retweetCount", 0),
        "like_count": getattr(tweet, "likeCount", 0),
        "reply_count": getattr(tweet, "replyCount", 0),
        "view_count": getattr(tweet, "viewCount", 0),
    }


async def collect_profile(api: API, handle: str) -> dict:
    """Collect tweets for a single profile."""
    try:
        user = await api.user_by_login(handle)
        if not user:
            return {"handle": handle, "error": "user_not_found", "tweets": []}

        tweets = []
        async for tweet in api.user_tweets(user.id, limit=MAX_TWEETS_PER_USER):
            if tweet.date and tweet.date.replace(tzinfo=timezone.utc) < CUTOFF:
                continue  # older than 24h, skip
            tweets.append(tweet_to_dict(tweet))

        return {
            "handle": handle,
            "user_id": str(user.id),
            "tweets": tweets,
        }
    except Exception as e:
        return {"handle": handle, "error": str(e), "tweets": []}


async def collect_all() -> dict:
    """Collect tweets from all monitored profiles."""
    api = API(pool_size=5)  # parallel profile lookups

    output = {
        "coletado_em": datetime.now(timezone.utc).isoformat(),
        "cutoff": CUTOFF.isoformat(),
        "total_perfis": len(PROFILES),
        "perfis_com_dados": 0,
        "perfis_com_erro": 0,
        "total_tweets": 0,
        "perfis": [],
    }

    # Process in batches to control concurrency
    sem = asyncio.Semaphore(5)  # max 5 concurrent

    async def collect_one(i, handle):
        async with sem:
            print(f"[{i}/{len(PROFILES)}] @{handle} ...", end=" ", flush=True)
            result = await collect_profile(api, handle)
            count = len(result["tweets"])
            if "error" in result and not result["tweets"]:
                print(f"❌ ({result['error'][:60]})")
            elif count:
                print(f"🟢 {count} tweets")
            else:
                print(f"⚪ sem tweets recentes")
            return result

    tasks = [collect_one(i, h) for i, h in enumerate(PROFILES, 1)]
    results = await asyncio.gather(*tasks)

    for r in results:
        if "error" in r and not r["tweets"]:
            output["perfis_com_erro"] += 1
        else:
            output["perfis_com_dados"] += 1
        output["total_tweets"] += len(r["tweets"])
        if r["tweets"]:  # only include profiles with data
            output["perfis"].append(r)

    return output


def main():
    dry_run = "--dry-run" in sys.argv

    output_path = OUTPUT_FILE
    for i, arg in enumerate(sys.argv):
        if arg == "--output" and i + 1 < len(sys.argv):
            output_path = Path(sys.argv[i + 1])

    result = asyncio.run(collect_all())

    # Print stats
    print(f"\n📊 {result['total_tweets']} tweets de {result['perfis_com_dados']} perfis "
          f"({result['perfis_com_erro']} erros)")

    if dry_run:
        return

    # Save full data
    output_path.parent.mkdir(parents=True, exist_ok=True)
    with open(output_path, "w", encoding="utf-8") as f:
        json.dump(result, f, ensure_ascii=False, indent=2)
    print(f"✅ Salvo em {output_path}")

    # Print compact summary for cron job context injection
    print("\n--- COLLECTION_SUMMARY_JSON ---")
    summary = {
        "coletado_em": result["coletado_em"],
        "total_tweets": result["total_tweets"],
        "perfis_ativos": len(result["perfis"]),
        "tweets": [],
    }
    for p in result["perfis"]:
        for t in p["tweets"]:
            t["_source_handle"] = p["handle"]
            summary["tweets"].append(t)
    print(json.dumps(summary, ensure_ascii=False))


if __name__ == "__main__":
    main()
