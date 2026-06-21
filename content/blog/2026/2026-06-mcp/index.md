---
title: "MCP Ponderings"
date: 2026-06-21
hideImages: true
featured: IMG_1518.jpeg
bsky: 3mosbctbyec2p
tags:
 - ai
 - mcp
atUri: "at://did:plc:r53zv4vpzeihop3aliwyejlu/site.standard.document/3mos64yogpf2w"
---

Agents are only as good as the access they have to accurate data and business functions. LLMs have a cut off point as to what they know - they're trained on a set of data and anything beyond that is unknown to them - therefore to build useful agents you need to provide a way for them to access data beyond that corpus.  This could be more your own business data or just more recent information. To enable this Anthropic [introduced Model Context Protocol][anthropic-blog] (MCP) as an open standard to build these connections to data-sources and tooling.  Since then, MCP has exploded into the most common way of providing tools to AI Agents.

![Bridge over Canal, Lancaster](IMG_1518.jpeg)

There are 2 main types of MCP Server - **local** which you download and run on your machine (just like a CLI tool) and **remote** that you connect to through a URL (just like an API).  They can both be configured and they both have their risks - so we need to consider how we safely manage these in our environment, building on how we control and manage APIs and software and APIs.


## Local MCP Servers (stdio)

There are thousands of pre-built MCP servers out there to download and use - some official but mostly unofficial community built servers created by interested developers or their AI Agents.  According to [Equixly] 43% of MCP servers contain command injection flaws and 30% permit unrestricted URL fetching, so it is important to understand what you are running. This highlights the fact that traditional security practices still apply to the agentic space - often more than ever.  Supply chain security and least privilege are more critical than ever when you have non-deterministic agent flows handling data through community tooling.

Often these are documented with a single command to download and run that you add to your agent config - using `npx` or `uvx`, however you can usually still download, build and run in the traditional way you would opensource projects to ensure you stick to the version you have verified. This way you have a level of control over the tools you are using but would still need to be sure to keep dependencies up to date.

## Remote MCP Servers (streamable-http / sse)

In a lot of ways use of a remote MCP server is very similar to using a third-party API as part of your application, in fact some places I've seen MCP tools provided where there wasn't previously even an API or access to the MCP be made easier than it was previously to get access to the API. There are however some key differences:

As Agents connect to MCP servers they will initialise a session and list the tools available with their specifications dynamically as a kind of discovery each session which is loaded into the agent context. The ensures they always have the latest tool definitions, can adapt accordingly and don't need to review a separate spec or changelog if the tooling is updated.

As they are being used in a non-deterministic process, you don't know up front what your agent will be sending them. For example agents build the tool call based on their language model, your input and the tool specification without formal object declarations, so it is all open to interpretation which may lead to unexpected sequences of tools or needing to retry to get parameter formats correct.  Whilst APIs would typically define input types using json schema, MCP defines tools with textual descriptions. One example I've seen was with timestamp formats where the backend the tool interacted with was expecting ISO8601 format but the agent was trying to use relative times.

## Security checklist for MCP

Ultimately, the responsibility for the security and integrity of these systems remains entirely with the user. Because agentic flows are non-deterministic the risk of an unintended action, triggered by a flawed community tool or a prompt injection, is higher than in traditional software.

- **Audit** the tooling - whether this is the source code downloaded or the provider of the hosted server - before you connect you should ensure you can trust it with your data.
- **Isolate** downloaded tools to limit the risk of command injection, for example running the MCP server within a Docker container controlling what they can access. For remote MCP servers, routing calls through a gateway gives similar control to restrict, observe and adjust interactions as needed.
- **Credentials** - Use dedicated credentials for MCP tooling that can be revoked, and apply the principle of least-privilege so they only have permissions they need.
- **Approvals** - Ensure that sensitive actions require a human approval.
- **Review** that the tools continue to work as you intended them to.

Also see [API Evangelist: MCP discovery and governance](https://apievangelist.com/2026/06/19/mcp-discovery-and-governance/)


[Equixly]: https://equixly.com/blog/2025/03/29/mcp-server-new-security-nightmare/
[anthropic-blog]: https://www.anthropic.com/news/model-context-protocol
