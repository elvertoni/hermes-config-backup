#!/usr/bin/env python3
from __future__ import annotations

from datetime import datetime, timezone
from pathlib import Path
import hashlib
import json
import shutil

import yaml

SOURCE = Path('/root/.hermes')
TARGET = Path('/root/hermes-config-backup')
INCLUDE_DIRS = [
    'skills',
    'scripts',
]
REDACT_KEYS = {
    'api_key', 'token', 'tokens', 'secret', 'secrets', 'password',
    'client_secret', 'access_token', 'refresh_token', 'authorization'
}


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def redact(value, key=None):
    if isinstance(value, dict):
        out = {}
        for k, v in value.items():
            if str(k).lower() in REDACT_KEYS:
                out[k] = 'REDACTED'
            else:
                out[k] = redact(v, k)
        return out
    if isinstance(value, list):
        return [redact(v, key) for v in value]
    if key and str(key).lower() in REDACT_KEYS:
        return 'REDACTED'
    if isinstance(value, str):
        lowered = value.lower()
        if value.startswith('sk-') or 'ghp_' in value or 'github_pat_' in value:
            return 'REDACTED'
        if 'token' in lowered or 'secret' in lowered:
            return 'REDACTED'
    return value


def copy_tree(src: Path, dst: Path):
    if dst.exists():
        shutil.rmtree(dst)
    shutil.copytree(src, dst)


def main():
    TARGET.mkdir(parents=True, exist_ok=True)

    manifest = {
        'generated_at_utc': datetime.now(timezone.utc).isoformat(),
        'source': str(SOURCE),
        'target': str(TARGET),
        'included_dirs': INCLUDE_DIRS,
        'included_files': ['config/config.redacted.yaml'],
        'excluded_sensitive_examples': [
            '.env', 'auth.json', 'google_token*.json', 'google_client_secret.json',
            'sessions/', 'logs/', 'state.db*', 'gateway_state.json'
        ],
        'files': [],
    }

    for rel in INCLUDE_DIRS:
        src = SOURCE / rel
        dst = TARGET / rel
        if src.exists():
            copy_tree(src, dst)

    cfg_src = SOURCE / 'config.yaml'
    cfg_dir = TARGET / 'config'
    cfg_dir.mkdir(parents=True, exist_ok=True)
    if cfg_src.exists():
        data = yaml.safe_load(cfg_src.read_text())
        redacted = redact(data)
        (cfg_dir / 'config.redacted.yaml').write_text(
            yaml.safe_dump(redacted, sort_keys=False, allow_unicode=True)
        )

    (TARGET / 'README.md').write_text(
        '# Hermes Config Backup\n\n'
        '- Origem: `/root/.hermes`\n'
        '- Tipo: backup sanitizado\n'
        '- Inclui: `skills/`, `scripts/`, `config/config.redacted.yaml`\n'
        '- Exclui: segredos, tokens, sessões, logs, bancos locais e estados efêmeros\n\n'
        'Objetivo: preservar skills, instruções, scripts e configuração sanitizada do Hermes em repositório Git privado.\n'
    )

    for path in sorted(TARGET.rglob('*')):
        if path.is_file() and '.git' not in path.parts:
            manifest['files'].append({
                'path': str(path.relative_to(TARGET)),
                'bytes': path.stat().st_size,
                'sha256': sha256(path),
            })

    (TARGET / 'manifest.json').write_text(json.dumps(manifest, ensure_ascii=False, indent=2) + '\n')
    print(json.dumps({'target': str(TARGET), 'files': len(manifest['files'])}, ensure_ascii=False))


if __name__ == '__main__':
    main()
