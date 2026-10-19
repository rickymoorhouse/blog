#!/usr/bin/env python3
"""
Warn when staged content has a front matter description or summary longer
than 160 characters (the limit used for the homepage meta description).

Reads the staged version of each added or modified Markdown file under
content/. Only ever warns: always exits 0 so it never blocks a commit.

Usage: python3 scripts/check_descriptions.py [file ...]
       (with no arguments, checks files staged in git)
"""
import subprocess
import sys

import yaml

LIMIT = 160
FIELDS = ("description", "summary")


def staged_files():
    out = subprocess.run(
        ["git", "diff", "--cached", "--name-only", "--diff-filter=AM", "--", "content/"],
        capture_output=True, text=True, check=True,
    ).stdout
    return [f for f in out.splitlines() if f.endswith(".md")]


def read_staged(path):
    return subprocess.run(
        ["git", "show", f":{path}"], capture_output=True, text=True, check=True,
    ).stdout


def front_matter(text):
    if not text.startswith("---"):
        return {}
    parts = text.split("\n---", 1)
    if len(parts) < 2:
        return {}
    try:
        data = yaml.safe_load(parts[0][3:])
    except yaml.YAMLError:
        return {}
    return data if isinstance(data, dict) else {}


def main(argv):
    if argv:
        files = [(f, open(f, encoding="utf-8").read()) for f in argv]
    else:
        files = [(f, read_staged(f)) for f in staged_files()]

    warnings = []
    for path, text in files:
        meta = front_matter(text)
        for field in FIELDS:
            value = meta.get(field)
            if isinstance(value, str) and len(value.strip()) > LIMIT:
                warnings.append(f"  {path}: {field} is {len(value.strip())} chars (limit {LIMIT})")

    if warnings:
        print(f"WARNING: front matter longer than {LIMIT} characters:")
        print("\n".join(warnings))
        print("Search engines may truncate these. Commit not blocked.")
    return 0


if __name__ == "__main__":
    try:
        sys.exit(main(sys.argv[1:]))
    except Exception as exc:  # never block a commit on a checker failure
        print(f"check_descriptions: skipped ({exc})")
        sys.exit(0)
