# Blog MCP server

A small, read-only [MCP](https://modelcontextprotocol.io) server for rickymoorhouse.uk. It lets AI assistants search and read the blog, microblog, talks and projects.

It only reads the published site, so it can run anywhere with internet access:

- `search.json` is built by Hugo (`themes/2026/layouts/home.search.json`). It holds one entry per post with the title, URL, date, section, tags, description and plain text.
- The server loads `search.json` into an in-memory [MiniSearch](https://lucaong.github.io/minisearch/) index. It reloads the index in the background every 10 minutes.
- `get_post` fetches a page's `index.md` from the site.

It uses the Streamable HTTP transport in stateless JSON mode. There are no sessions and no auth, and the endpoint is `/mcp`.

## Tools

| Tool | Arguments | Returns |
| --- | --- | --- |
| `search_posts` | `query`, plus optional `section` (`blog`, `microblog`, `talks`, `projects`), `tag` and `limit` (default 10, max 50) | Matching posts with title, URL, Markdown URL, date, section, category, tags, description and score |
| `get_post` | `url` of a page on the site | The page as Markdown |
| `list_recent` | optional `section` and `limit` | The newest posts, in the same shape as search results |

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
