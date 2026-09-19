#!/usr/bin/env bash
set -Eeuo pipefail

ROOT_DIR="$(CDPATH= cd -- "$(dirname -- "${BASH_SOURCE[0]}")/.." && pwd)"

# Keep local macOS publishing convenient without making Keychain a Linux dependency.
if [[ -z "${BUNNYCDN_PASSWORD:-}" ]] && command -v security >/dev/null 2>&1; then
    BUNNYCDN_PASSWORD="$(security find-generic-password -s bunny-storage -w)"
    export BUNNYCDN_PASSWORD
fi
if [[ -z "${BUNNYCDN_APIKEY:-}" ]] && command -v security >/dev/null 2>&1; then
    BUNNYCDN_APIKEY="$(security find-generic-password -s bunny-apikey -w)"
    export BUNNYCDN_APIKEY
fi

: "${BUNNYCDN_PASSWORD:?Set BUNNYCDN_PASSWORD or store bunny-storage in the macOS Keychain}"
: "${BUNNYCDN_APIKEY:?Set BUNNYCDN_APIKEY or store bunny-apikey in the macOS Keychain}"

BUNNYCDN_USERNAME="${BUNNYCDN_USERNAME:-rm-uk-standard}"
BUNNYCDN_PULLZONE="${BUNNYCDN_PULLZONE:-3422848}"

if [[ ! -d "$ROOT_DIR/public" ]]; then
    printf 'Generated site not found. Run scripts/build.sh first.\n' >&2
    exit 1
fi
if ! command -v duck >/dev/null 2>&1; then
    printf 'Required deployment command not found: duck\n' >&2
    printf 'Install Cyberduck CLI or provide a compatible deployment wrapper.\n' >&2
    exit 1
fi

cd "$ROOT_DIR"

duck -y \
    --username "$BUNNYCDN_USERNAME" \
    --password "$BUNNYCDN_PASSWORD" \
    --existing overwrite \
    --upload ftps://uk.storage.bunnycdn.com/ ./public/

curl --fail-with-body --silent --show-error \
    -X POST \
    -H "AccessKey: ${BUNNYCDN_APIKEY}" \
    "https://api.bunny.net/pullzone/${BUNNYCDN_PULLZONE}/purgeCache"

printf 'Deployment and cache purge completed successfully.\n'
