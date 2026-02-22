---
title: "Building an AI Agent: From Inspiration to Implementation"
date: 2026-02-16
layout: blog
tags:
 - ai
 - coding
 - golang
 - agent
 - architecture
---

I've been fascinated by the idea of AI agents for a while now - programs that can not just chat, but actually _do_ things. A few weeks back I came across Clawdbot - now called [OpenClaw](https://openclaw.ai) and it clicked something in my brain. This had a great potential for proactive workflows with a regular trigger to identify things that needed doing and the ability to extend itself with additional code and updates to it's own configuration.  Very powerful, but also very risky if not controlled. I set this up intially as it's own user account and then fairly soon moved it into an isolated VM. 

I really liked the potential here but wasn't comfortable with the complexity of the code and the power I was giving it or would need to give it to do more interesting tasks - I've still not let it access calendar or e-mail for example. However if I could build something I could read all the code for and understand - with my own selection of controls and tools that are limited according to my own sense of risk level. 

So rather than just using someone elses platform I embarked on building something smaller and more personal that I could tune to the things I wanted it to do. This became a great learning experience in understanding the basics at the core of what is needed in an Agent but also how this can get much more complex as you start to deal with things like memory and control.

<!--more-->

## Why Go?

Python would have been the obvious choice. It's the lingua franca of AI, with libraries for everything, but I wanted to start with API calls rather than libraries anyway and Go offered something different:

- **Single binary deployment** - no virtual environments, no dependency hell
- **Straightforward concurrency** - agents need to do multiple things at once
- **Static typing** - catching mistakes at compile time matters when your agent is taking real actions
- **Simple tool integration** - calling external programs is trivial


## The Architecture

The agent follows a pattern you'll recognise if you've looked at OpenClaw or similar frameworks:

1. **Model** - The brain. Currently I'm switching between Ollama, MiniMax and Claude all using their Anthropic compatible API
2. **Planner** - Takes the user's request and figures out what steps are needed
3. **Executor** - Runs the planned steps, handling tool calls and results
4. **Tools** - The verbs the agent can use (files, commands, web search, etc.)

```
User Request → Planner → [Tool Calls] → Executor → Results
                   ↑                         │
                   └────── Feedback ←────────┘
```

The key insight from OpenClaw that shaped this was **deliberate action**. The agent doesn't just guess what to do - it reasons about the next step, executes it, observes the result, and decides what to do next. That loop is the heart of it.

## The Tool Selection

So far I've created a set of basic tools:

| Tool | Purpose |
|------|---------|
| `read_file` / `edit_file` | Working with code and notes |
| `exec_cmd` | Running shell commands |
| `list_files` | Exploring directory structures |
| `web_search` / `web_fetch` | Research without leaving the terminal |
| `todoist` | Task list for the agent to work on without always being directly prompted |

The interesting part wasn't adding tools - it was **deciding what not to add**. Every tool is a potential attack surface or a source of confusion. The discipline of a small, thoughtful toolbox is more valuable than a big one.

## Lessons from Building It

### Context is everything

The agent is only as good as what it knows about the world it's operating in. Early versions missed crucial details because I didn't pass the right context to the model. Now I spend more time thinking about what context to provide than about the tool infrastructure itself.

### Tool design matters enormously

Badly designed tools create bad agent behaviour. The model will find the problems with the tools and either hit them multiple times causing more to clean up or work around them in interesting new ways. A tool that returns too much information overwhelms the context. Too little, and the agent is flying blind. The best tools do one thing well and return structured, predictable output. One of the things I found that helped here was when the agent was struggling with the tools - either through bugs or a lack of clarity I had it look at improving them in context so the specific error fed into the solution.  An example of this was it kept trying to use the exec tool to write new files and hitting issues as my protections were blocking multi-line pipes, where as I'd intended this to be done through the edit tool - so asked the agent to improve the description and metadata for the edit tool to make it clear it could be used for this. 

### Trust but verify

The agent can take actions - that's the point. But it needs guardrails. I've built in permissions and observability so I can see what it's trying to do before it does something irreversible. The goal is helpful, not dangerous. 

## What's Next

Right now the agent is genuinely useful for my workflow. It writes drafts, fetches information, organises files, and saves me clicks. But there's more to do:

- **Memory** - I'm storing memory in markdown but want to explore doing something better here for easier retrieval
- **Multi-step tool composition** - chaining tools intelligently - often today it feels like there are more steps used than really necessary so seeing potential for optimisation
- **Better planning** - fewer back-and-forth iterations

The thing I'm most proud of isn't any single feature. It's that it exists, that I built something that actually works, and that it reflects how I think about AI: not as magic, but as a tool. 
I'll probably share more findings as I experiment more - for now this is working for me as a collaborator on code development (including it's own code base) and a research assistant.

---

_The code lives in a private repo for now as this is intended as a personal agent not a framework, but the concepts here are universal. If you're thinking about building an agent, start small, choose your tools carefully, and remember: the goal is to build something that helps you._
