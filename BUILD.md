# Build And Publish

The project uses `mise` to pin the core local tools on macOS and Linux.

## Tools

Install `mise`, then install the project tools:

```sh
mise install
```

The repository manages Hugo Extended, Python, and `jq`. Pagefind is currently kept as an explicit binary dependency because its release artifacts need platform-specific selection. Set `PAGEFIND_BIN` when it is not available on `PATH`.

## Build

Build, generate flight data, build the Pagefind index, and validate JSON outputs:

```sh
mise run build
```

The equivalent direct command is:

```sh
./scripts/build.sh
```

## Blogroll

`data/blogroll.yaml` drives `/blogroll/` and `/.well-known/following.opml`. Import feed reader OPML exports (several at once is fine) with:

```sh
python3 scripts/import_opml.py --dry-run export1.opml export2.opml   # preview
python3 scripts/import_opml.py export1.opml export2.opml
```

Duplicate feeds are skipped (ignoring http/https, `www.`, trailing slashes and tracking parameters), and existing entries are never overwritten or reordered; only a missing `htmlUrl` or `description` is filled in. The innermost OPML folder becomes the category.

Check every feed and site in the blogroll for broken links, redirects, non-feeds, stale feeds and secret-looking URLs (network access, so it isn't part of the build; exits 1 on broken links):

```sh
mise run check-blogroll                                         # summary and problems
python3 scripts/check_blogroll.py --report ~/blog-feed-check.md # full Markdown report
```

## Publish

Publishing requires Bunny credentials. On macOS, the deploy script reads the existing `bunny-storage` and `bunny-apikey` Keychain entries. On Linux, provide environment variables:

```sh
export BUNNYCDN_PASSWORD='...'
export BUNNYCDN_APIKEY='...'
mise run publish
```

The publish task builds and validates before uploading `public/` and purging the Bunny pull-zone cache.

## Pre-commit hook

The tracked hook in `.githooks/pre-commit` runs `scripts/validate.py` (blocking) and
`scripts/check_descriptions.py`, which warns without blocking when a staged post's
front matter `description` or `summary` is over 160 characters. Enable it once per clone:

```sh
git config core.hooksPath .githooks
```
