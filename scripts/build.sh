#!/usr/bin/env bash
set -Eeuo pipefail

ROOT_DIR="$(CDPATH= cd -- "$(dirname -- "${BASH_SOURCE[0]}")/.." && pwd)"
HUGO_BIN="${HUGO_BIN:-hugo}"
PAGEFIND_BIN="${PAGEFIND_BIN:-pagefind}"
PYTHON_BIN="${PYTHON_BIN:-python3}"
JQ_BIN="${JQ_BIN:-jq}"

require_command() {
    if ! command -v "$1" >/dev/null 2>&1; then
        printf 'Required command not found: %s\n' "$1" >&2
        printf 'Install the project tools with: mise install\n' >&2
        exit 1
    fi
}

require_command "$HUGO_BIN"
require_command "$PAGEFIND_BIN"
require_command "$PYTHON_BIN"
require_command "$JQ_BIN"

cd "$ROOT_DIR"

"$HUGO_BIN" \
    --gc \
    --minify \
    --cleanDestinationDir \
    --printPathWarnings

"$PYTHON_BIN" scripts/generate_flights.py

"$PAGEFIND_BIN"

"$JQ_BIN" -e . public/index.json >/dev/null
"$JQ_BIN" -e . public/activitypub/index.json >/dev/null
"$JQ_BIN" -e . public/map/index.json >/dev/null
"$JQ_BIN" -e . public/flights.json >/dev/null

printf 'Build and output validation completed successfully.\n'
