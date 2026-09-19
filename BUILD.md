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

## Publish

Publishing requires Bunny credentials. On macOS, the deploy script reads the existing `bunny-storage` and `bunny-apikey` Keychain entries. On Linux, provide environment variables:

```sh
export BUNNYCDN_PASSWORD='...'
export BUNNYCDN_APIKEY='...'
mise run publish
```

The publish task builds and validates before uploading `public/` and purging the Bunny pull-zone cache.
