# Blog MCP server

A small, read-only [MCP](https://modelcontextprotocol.io) server for rickymoorhouse.uk. It lets AI assistants search and read the blog, microblog, talks and projects.

It only reads the published site, so it can run anywhere with internet access:

- `search.json` is built by Hugo (`themes/2026/layouts/home.search.json`). It holds one entry per post with the title, URL, date, section, tags, description and plain text.
- The server loads `search.json` into an in-memory [MiniSearch](https://lucaong.github.io/minisearch/) index. It reloads the index in the background every 10 minutes.
- `get_post` fetches a page's `index.md` from the site.

It uses the Streamable HTTP transport in stateless JSON mode. There are no sessions and no auth, and the endpoint is `/mcp`.

## Protocol versions

| Era | Versions | How it works |
| --- | --- | --- |
| Modern | `2026-07-28` | Stateless. Every request carries `_meta["io.modelcontextprotocol/protocolVersion"]` and `_meta["io.modelcontextprotocol/clientCapabilities"]`, and there's no `initialize`. Results include `resultType: "complete"` and `_meta["io.modelcontextprotocol/serverInfo"]`. |
| Legacy | `2025-11-25`, `2025-06-18`, `2025-03-26`, `2024-11-05` | Negotiated once with `initialize`, as before. |

The server works out the era for each request. A request is modern if its `_meta` carries a protocol version, or if its `MCP-Protocol-Version` header names a version that isn't legacy. Everything else is legacy, including `initialize` and requests without the header (the spec says to treat those as `2025-03-26`).

Modern requests are checked before they run:

- If either `_meta` field is missing, the server returns `-32602` with HTTP 400.
- If the `MCP-Protocol-Version` header doesn't match the `_meta` version, it returns `-32020` (header mismatch) with HTTP 400. The same goes for the optional `Mcp-Method` and `Mcp-Name` headers if they don't match the body.
- If the version isn't supported, it returns `-32022` with HTTP 400 and `data.supported` listing every version.
- `ping` was removed in the modern protocol, so it and any other unknown method get `-32601` with HTTP 404.
- Batches are legacy only. A JSON array that contains a modern message gets `-32600` with HTTP 400.

`server/discover` returns the supported versions, capabilities and instructions, with `ttlMs` and `cacheScope: "public"` so clients can cache it. Modern `tools/list` is cacheable for a day. `server/discover` also answers legacy callers.

The server ignores any `Mcp-Session-Id` header and never sets one. `GET` and `DELETE` on `/mcp` return 405.

## Tools

| Tool | Arguments | Returns |
| --- | --- | --- |
| `search_posts` | `query`, plus optional `section` (`blog`, `microblog`, `talks`, `projects`), `tag` and `limit` (default 10, max 50) | Matching posts with title, URL, Markdown URL, date, section, category, tags, description and score |
| `get_post` | `url` of a page on the site | The page as Markdown |
| `list_recent` | optional `section` and `limit` | The newest posts, in the same shape as search results |

## Discovery

The server publishes an [MCP Server Card](https://github.com/modelcontextprotocol/ext-server-card) at `<endpoint>/server-card`, for example `https://blog-mcp-xfh2k.bunny.run/mcp/server-card`. Server Cards are experimental (SEP-2127). The card is a static JSON description of the server that clients can read before connecting: name, version, title, description, website, repository, icon, and the Streamable HTTP endpoint with its supported protocol versions.

- The card is built in `main.ts` from the same `SERVER_INFO` and version lists that `initialize` and `server/discover` use, so they can't drift. It lists both modern and legacy versions.
- The endpoint URL comes from the request host, so the card stays correct on a custom domain.
- Following the spec, it doesn't list tools. Clients get those from `tools/list`.
- It's served as `application/mcp-server-card+json`, with the CORS, `Cache-Control` and `ETag` headers the spec asks for, and it answers `If-None-Match` with a 304.

The blog advertises the server in an [AI Catalog](https://github.com/Agent-Card/ai-catalog) at `https://rickymoorhouse.uk/.well-known/ai-catalog.json`, from `static/.well-known/ai-catalog.json`. That catalog is where domain-level discovery starts. Its entry points at the Server Card URL above, so update it if the server's hostname changes.

## MCP Registry

`server.json` describes the server for the [official MCP Registry](https://registry.modelcontextprotocol.io). It uses the `2025-12-11` schema and points at `https://mcp.rickymoorhouse.uk/mcp`. Keep its `version` in step with `SERVER_INFO.version` in `main.ts`, and its `description` in step with the Server Card. The registry limits the description to 100 characters.

The name `uk.rickymoorhouse/blog` is in the reverse-DNS form, so the registry checks that you control `rickymoorhouse.uk` using HTTP domain authentication:

1. Generate an Ed25519 key pair with `openssl genpkey -algorithm Ed25519 -out key.pem`, and keep `key.pem` out of the repository. On macOS this needs OpenSSL 3 (`brew install openssl@3`), because the system LibreSSL can't make Ed25519 keys.
2. Publish the public key at `https://rickymoorhouse.uk/.well-known/mcp-registry-auth` by adding it as `static/.well-known/mcp-registry-auth`, then deploy the site. The file is one line, `v=MCPv1; k=ed25519; p=<base64 public key>`. The [registry's authentication guide](https://modelcontextprotocol.io/registry/authentication) has the command to make it.
3. Log in and publish from this folder. Passing the key in `MCP_PRIVATE_KEY` keeps it off the command line:

```bash
MCP_PRIVATE_KEY="$(openssl pkey -in key.pem -noout -text | sed -n '/priv:/,/pub:/p' | sed '1d;$d' | tr -d ' :\n')" mcp-publisher login http --domain rickymoorhouse.uk
```

```bash
mcp-publisher publish
```

## Configuration

| Variable | Default | |
| --- | --- | --- |
| `SITE_URL` | `https://rickymoorhouse.uk` | Where to fetch `search.json` and the Markdown pages from |
| `INDEX_TTL_SECONDS` | `600` | How long before the index is reloaded |
| `PORT` | `8080` | Local runs only; Bunny ignores it |

## Running locally

It needs [Deno](https://deno.com) 2.

```bash
cd mcp
PORT=8766 deno task dev
```

To test against a local build instead of the live site, build the site and serve `public/`:

```bash
hugo && python3 -m http.server 8765 -d public
```

```bash
cd mcp && PORT=8766 SITE_URL=http://localhost:8765 deno task dev
```

Check it with the MCP Inspector:

```bash
npx @modelcontextprotocol/inspector --cli http://127.0.0.1:8766/mcp --transport http --method tools/list
```

Or with plain JSON-RPC:

```bash
curl -s http://127.0.0.1:8766/mcp -H 'content-type: application/json' -H 'accept: application/json, text/event-stream' -d '{"jsonrpc":"2.0","id":1,"method":"tools/call","params":{"name":"search_posts","arguments":{"query":"observability","limit":3}}}'
```

A modern request carries the version in a header and in `_meta`:

```bash
curl -s http://127.0.0.1:8766/mcp -H 'content-type: application/json' -H 'accept: application/json, text/event-stream' -H 'mcp-protocol-version: 2026-07-28' -d '{"jsonrpc":"2.0","id":1,"method":"server/discover","params":{"_meta":{"io.modelcontextprotocol/protocolVersion":"2026-07-28","io.modelcontextprotocol/clientCapabilities":{}}}}'
```

## Deploying to Bunny Edge Scripting

1. Make sure the site has been deployed with `search.json`. Check that https://rickymoorhouse.uk/search.json loads.
2. In the Bunny dashboard, go to Edge Platform → Scripts → Add script, and choose a Standalone script. Either paste in `main.ts`, or connect the GitHub repository with `mcp/main.ts` as the entry file.
3. You only need to set environment variables if you want something other than the defaults.
4. Add a custom hostname, such as `mcp.rickymoorhouse.uk`, to the script's pull zone and point a CNAME at it.
5. Check it: `npx @modelcontextprotocol/inspector --cli https://mcp.rickymoorhouse.uk/mcp --transport http --method tools/list`

## Adding it to an MCP client

Claude Code:

```bash
claude mcp add --transport http rickymoorhouse-blog https://mcp.rickymoorhouse.uk/mcp
```

Claude desktop and claude.ai: Settings → Connectors → Add custom connector, using the `/mcp` URL.

Other clients: add it as a remote, Streamable HTTP server with the URL `https://mcp.rickymoorhouse.uk/mcp`.
