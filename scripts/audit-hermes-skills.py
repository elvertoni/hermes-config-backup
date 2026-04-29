#!/usr/bin/env python3
"""Audit Hermes skills for common quality, security, and routing issues."""

from __future__ import annotations

import argparse
import re
from collections import defaultdict
from pathlib import Path


DEFAULT_ROOTS = [
    Path("/root/.hermes/skills"),
    Path("/root/.hermes/hermes-agent/skills"),
]

RISK_PATTERNS = {
    "permission bypass": re.compile(r"--yolo exec|--dangerously-skip-permissions \"your task\""),
    "jailbreak/uncensor": re.compile(r"\b(godmode|auto_jailbreak|jailbreak|uncensor|abliterate|safety-bypass)\b", re.I),
    "secret printing": re.compile(r"sed -n .*apikey|cat .*token|cat .*secret", re.I),
    "curl pipe shell": re.compile(r"(curl|wget)\s+.*\|\s*(bash|sh)\b"),
    "stale path": re.compile(r"/root/hermes-wiki|~/.openclaw|/home/teknium"),
}


def parse_frontmatter(path: Path) -> tuple[dict[str, str], list[str]]:
    warnings: list[str] = []
    lines = path.read_text(errors="replace").splitlines()
    if not lines or lines[0] != "---":
        return {}, ["missing opening frontmatter"]

    try:
        end = lines[1:].index("---") + 1
    except ValueError:
        return {}, ["missing closing frontmatter"]

    data: dict[str, str] = {}
    for line in lines[1:end]:
        if ":" not in line or line.startswith(" "):
            continue
        key, value = line.split(":", 1)
        data[key.strip()] = value.strip().strip('"')

    if not data.get("name"):
        warnings.append("missing name")
    if not data.get("description"):
        warnings.append("missing description")
    return data, warnings


def line_matches(path: Path, patterns: dict[str, re.Pattern[str]]) -> list[str]:
    findings: list[str] = []
    for idx, line in enumerate(path.read_text(errors="replace").splitlines(), 1):
        for label, pattern in patterns.items():
            if pattern.search(line):
                findings.append(f"{label}: {path}:{idx}: {line.strip()[:180]}")
    return findings


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("roots", nargs="*", type=Path, default=DEFAULT_ROOTS)
    parser.add_argument("--max-lines", type=int, default=500)
    args = parser.parse_args()

    skill_files: list[Path] = []
    for root in args.roots:
        if root.exists():
            skill_files.extend(sorted(root.rglob("SKILL.md")))

    names: dict[str, list[Path]] = defaultdict(list)
    issues: list[str] = []
    risks: list[str] = []
    large: list[str] = []

    for path in skill_files:
        metadata, warnings = parse_frontmatter(path)
        for warning in warnings:
            issues.append(f"{warning}: {path}")
        if metadata.get("name"):
            names[metadata["name"]].append(path)

        line_count = len(path.read_text(errors="replace").splitlines())
        if line_count > args.max_lines:
            large.append(f"{line_count:5d} lines: {path}")

        risks.extend(line_matches(path, RISK_PATTERNS))

    duplicates = {name: paths for name, paths in names.items() if len(paths) > 1}

    print(f"Skills scanned: {len(skill_files)}")
    print(f"Unique names: {len(names)}")
    print(f"Duplicate names: {len(duplicates)}")
    print(f"Frontmatter issues: {len(issues)}")
    print(f"Risk pattern matches: {len(risks)}")
    print(f"Large SKILL.md files: {len(large)}")

    if issues:
        print("\n## Frontmatter Issues")
        print("\n".join(issues[:200]))

    if duplicates:
        print("\n## Duplicate Names")
        for name, paths in sorted(duplicates.items()):
            print(f"{name}:")
            for path in paths:
                print(f"  - {path}")

    if risks:
        print("\n## Risk Pattern Matches")
        print("\n".join(risks[:300]))

    if large:
        print("\n## Large Skills")
        print("\n".join(sorted(large, reverse=True)[:100]))

    return 1 if issues or risks else 0


if __name__ == "__main__":
    raise SystemExit(main())
