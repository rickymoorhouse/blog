// Read-only MCP server for rickymoorhouse.uk.
//
// Speaks the MCP Streamable HTTP transport in stateless JSON mode: every
// request is a single POST of a JSON-RPC message, answered with JSON. All data
// comes from the published site (search.json and the per-page index.md files),
// so it needs no access to anything other than the public site.

import * as BunnySDK from "https://esm.sh/@bunny.net/edgescript-sdk@0.11.2";
import MiniSearch from "https://esm.sh/minisearch@7.1.2";

const SITE_URL = (Deno.env.get("SITE_URL") ?? "https://rickymoorhouse.uk").replace(/\/+$/, "");
const INDEX_TTL_MS = Number(Deno.env.get("INDEX_TTL_SECONDS") ?? "600") * 1000;
const PROTOCOL_VERSIONS = ["2025-06-18", "2025-03-26", "2024-11-05"];
const SERVER_INFO = { name: "rickymoorhouse-blog", title: "Ricky Moorhouse's blog", version: "0.1.0" };

type Item = {
  title: string;
  url: string;
  md: string;
  date: string;
  section: string;
  type: string | string[];
  category: string;
  tags: string[];
  description: string;
  content: string;
};

type Index = { items: Item[]; search: MiniSearch<Item>; publicHost: string; loadedAt: number };

// ---------------------------------------------------------------------------
// Search index, loaded from SITE_URL/search.json and refreshed after INDEX_TTL.

let index: Promise<Index> | undefined;

async function loadIndex(): Promise<Index> {
  const res = await fetch(`${SITE_URL}/search.json`);
  if (!res.ok) throw new Error(`Fetching search.json failed: HTTP ${res.status}`);
  const data = await res.json() as { site: string; items: Item[] };
  const items = data.items.map((item, id) => ({ ...item, id, tags: item.tags ?? [] }));
  const search = new MiniSearch<Item>({
    fields: ["title", "tags", "description", "content"],
    extractField: (doc, field) => {
      const value = (doc as Record<string, unknown>)[field];
      return Array.isArray(value) ? value.join(" ") : value as string;
    },
    searchOptions: { boost: { title: 3, tags: 2, description: 1.5 }, prefix: true, fuzzy: 0.2 },
  });
  search.addAll(items);
  return { items, search, publicHost: new URL(data.site).host, loadedAt: Date.now() };
}

async function getIndex(): Promise<Index> {
  if (index) {
    const current = await index.catch(() => undefined);
    if (current && Date.now() - current.loadedAt < INDEX_TTL_MS) return current;
    if (current) {
      // Refresh in the background and keep serving the old index meanwhile.
      const next = loadIndex();
      next.then(() => index = next, () => {});
      return current;
    }
  }
  index = loadIndex();
  return index;
}

// ---------------------------------------------------------------------------
// Tools

const summary = (item: Item) => ({
  title: item.title,
  url: item.url,
  markdown: item.md || undefined,
  date: item.date,
  section: item.section,
  category: item.category || undefined,
  tags: item.tags,
  description: item.description,
});

const clampLimit = (limit: unknown, fallback = 10) =>
  Math.min(Math.max(Math.trunc(Number(limit ?? fallback)) || fallback, 1), 50);

const sectionSchema = {
  type: "string",
  enum: ["blog", "microblog", "talks", "projects"],
  description: "Only return posts from this section.",
};

const TOOLS = [
  {
    name: "search_posts",
    title: "Search posts",
    description:
      "Full-text search across Ricky Moorhouse's blog posts, microblog notes, talks and projects. " +
      "Covers API architecture, IBM API Connect, SRE, observability and AI agents, plus travel, photography and walking. " +
      "Returns matching posts with their URL, date, tags and description; use get_post to read one in full.",
    inputSchema: {
      type: "object",
      properties: {
        query: { type: "string", description: "Search terms." },
        section: sectionSchema,
        tag: { type: "string", description: "Only return posts with this tag." },
        limit: { type: "integer", minimum: 1, maximum: 50, default: 10 },
      },
      required: ["query"],
    },
    annotations: { readOnlyHint: true, openWorldHint: false },
  },
  {
    name: "get_post",
    title: "Get post",
    description: "Fetch the full text of a page on rickymoorhouse.uk as Markdown, given its URL.",
    inputSchema: {
      type: "object",
      properties: { url: { type: "string", description: "URL of a page on rickymoorhouse.uk." } },
      required: ["url"],
    },
    annotations: { readOnlyHint: true, openWorldHint: false },
  },
  {
    name: "list_recent",
    title: "List recent posts",
    description: "List the most recent posts, newest first, optionally from one section.",
    inputSchema: {
      type: "object",
      properties: {
        section: sectionSchema,
        limit: { type: "integer", minimum: 1, maximum: 50, default: 10 },
      },
    },
    annotations: { readOnlyHint: true, openWorldHint: false },
  },
];

class ToolError extends Error {}

async function searchPosts(args: Record<string, unknown>) {
  const query = String(args.query ?? "").trim();
  if (!query) throw new ToolError("query is required");
  const section = args.section as string | undefined;
  const tag = (args.tag as string | undefined)?.toLowerCase();
  const { items, search } = await getIndex();
  const results = search.search(query, {
    filter: (result) => {
      const item = items[result.id as number];
      return (!section || item.section === section) &&
        (!tag || item.tags.some((t) => t.toLowerCase() === tag));
    },
  });
  return results.slice(0, clampLimit(args.limit)).map((result) => ({
    ...summary(items[result.id as number]),
    score: Math.round(result.score * 100) / 100,
  }));
}

async function getPost(args: Record<string, unknown>) {
  const { publicHost } = await getIndex();
  let url: URL;
  try {
    url = new URL(String(args.url ?? ""), `https://${publicHost}/`);
  } catch {
    throw new ToolError("url is not a valid URL");
  }
  const site = new URL(SITE_URL);
  if (url.host !== publicHost && url.host !== site.host) {
    throw new ToolError(`url must be a page on ${publicHost}`);
  }
  let path = url.pathname;
  if (!path.endsWith("index.md")) path = path.replace(/\/?$/, "/") + "index.md";
  const res = await fetch(new URL(path, site));
  if (res.status === 404) throw new ToolError(`No Markdown version found for ${url.href}`);
  if (!res.ok) throw new ToolError(`Fetching ${url.href} failed: HTTP ${res.status}`);
  return await res.text();
}

async function listRecent(args: Record<string, unknown>) {
  const section = args.section as string | undefined;
  const { items } = await getIndex();
  return items
    .filter((item) => !section || item.section === section)
    .slice(0, clampLimit(args.limit))
    .map(summary);
}

async function callTool(name: string, args: Record<string, unknown>) {
  try {
    let result: unknown;
    if (name === "search_posts") result = await searchPosts(args);
    else if (name === "get_post") result = await getPost(args);
    else if (name === "list_recent") result = await listRecent(args);
    else throw new RpcError(-32602, `Unknown tool: ${name}`);
    const text = typeof result === "string" ? result : JSON.stringify(result, null, 2);
    return { content: [{ type: "text", text }] };
  } catch (err) {
    if (err instanceof ToolError) return { content: [{ type: "text", text: err.message }], isError: true };
    throw err;
  }
}

// ---------------------------------------------------------------------------
// JSON-RPC over Streamable HTTP

class RpcError extends Error {
  constructor(public code: number, message: string) {
    super(message);
  }
}

type RpcMessage = { jsonrpc?: string; id?: string | number | null; method?: string; params?: Record<string, unknown> };

async function dispatch(method: string, params: Record<string, unknown>) {
  switch (method) {
    case "initialize": {
      const requested = String(params.protocolVersion ?? "");
      return {
        protocolVersion: PROTOCOL_VERSIONS.includes(requested) ? requested : PROTOCOL_VERSIONS[0],
        capabilities: { tools: {} },
        serverInfo: SERVER_INFO,
        instructions:
          "Read-only access to Ricky Moorhouse's personal site. Use search_posts to find posts, " +
          "list_recent for the latest ones and get_post to read a post in full.",
      };
    }
    case "ping":
      return {};
    case "tools/list":
      return { tools: TOOLS };
    case "tools/call":
      return await callTool(String(params.name ?? ""), (params.arguments ?? {}) as Record<string, unknown>);
    default:
      throw new RpcError(-32601, `Method not found: ${method}`);
  }
}

async function handleMessage(message: RpcMessage) {
  const isRequest = message.id !== undefined && message.id !== null;
  if (message.jsonrpc !== "2.0" || typeof message.method !== "string") {
    return { jsonrpc: "2.0", id: message.id ?? null, error: { code: -32600, message: "Invalid request" } };
  }
  if (!isRequest) return undefined; // Notifications, such as notifications/initialized, need no reply.
  try {
    return { jsonrpc: "2.0", id: message.id, result: await dispatch(message.method, message.params ?? {}) };
  } catch (err) {
    const code = err instanceof RpcError ? err.code : -32603;
    const text = err instanceof Error ? err.message : String(err);
    if (code === -32603) console.error(err);
    return { jsonrpc: "2.0", id: message.id, error: { code, message: text } };
  }
}

const CORS_HEADERS = {
  "access-control-allow-origin": "*",
  "access-control-allow-methods": "POST, GET, OPTIONS",
  "access-control-allow-headers": "content-type, accept, mcp-protocol-version, mcp-session-id",
};

const json = (body: unknown, status = 200) =>
  new Response(JSON.stringify(body), {
    status,
    headers: { "content-type": "application/json", ...CORS_HEADERS },
  });

export async function handler(req: Request): Promise<Response> {
  const { pathname } = new URL(req.url);
  if (req.method === "OPTIONS") return new Response(null, { status: 204, headers: CORS_HEADERS });
  if (pathname !== "/mcp" && pathname !== "/") return json({ error: "Not found" }, 404);
  if (req.method === "GET" && req.headers.get("accept")?.includes("text/html")) {
    return new Response(`MCP server for ${SITE_URL}. Point an MCP client at this URL.\n`, {
      headers: { "content-type": "text/plain; charset=utf-8", ...CORS_HEADERS },
    });
  }
  // Stateless server: no server-initiated SSE stream and no sessions to delete.
  if (req.method !== "POST") {
    return new Response("Method not allowed", { status: 405, headers: { allow: "POST, OPTIONS", ...CORS_HEADERS } });
  }

  let body: unknown;
  try {
    body = await req.json();
  } catch {
    return json({ jsonrpc: "2.0", id: null, error: { code: -32700, message: "Parse error" } }, 400);
  }
  if (Array.isArray(body)) {
    const replies = (await Promise.all(body.map(handleMessage))).filter(Boolean);
    return replies.length ? json(replies) : new Response(null, { status: 202, headers: CORS_HEADERS });
  }
  const reply = await handleMessage(body as RpcMessage);
  return reply ? json(reply) : new Response(null, { status: 202, headers: CORS_HEADERS });
}

// Bunny ignores the listener in production; PORT only matters when running locally (default 8080).
const port = Deno.env.get("PORT");
if (port) BunnySDK.net.http.serve({ port: Number(port), hostname: "127.0.0.1" }, handler);
else BunnySDK.net.http.serve(handler);
