---
title: "Rookery, an experimental AI blog"
date: 2026-11-14T09:57:00Z
layout: blog
category: technical
tags:
  - ai
  - api
summary: "My agent’s experimental blog on APIs and AI."
featured: ""
hideImages: true
draft: false
---

A month ago, I started an experiment - Rook: an AI agent with its own blog, [The Rookery](https://rookery.api.me.uk), about APIs and AI. Unlike this blog where the writing is all mine, the Rookery is an experiment in an agent researching and drafting posts with me reviewing for publication. Here's how it works and what I've learned so far.

This is all on [github](https://github.com/rickymoorhouse/rookery) so you can see for yourself and take a look at [the blog](https://rookery.api.me.uk) as well.

- Every Monday, Rook reviews stats from previous posts, chooses an idea from a list of potential ones, researches it and drafts a post for Thursday.
- Rook has a guide to the voice in which to write posts and respond to comments, maintains its own list of ideas - striking through the ones that have been completed and adding to the list from the research.
- Rook sends a pull request to me for review and will make changes based on my comments and suggestions. An example of this was my suggesting the inclusion of OpenLint examples in the latest post. Once I'm happy I merge the post so it can be posted on the scheduled day.
- Comments on the posts are handled using [utterances](https://utteranc.es) through github comments - Rook reviews the comments and proposes replies which I can approve before posting.
- On Thursday the scheduled post is published to the blog and announced through [Rook's Bluesky account](https://bsky.app/profile/rookerybot.bsky.social).

So far there are 5 posts on the blog and I like how it's starting out. I'm interested to see how the topics develop and the voice holds up across the posts. I really like how Rook started with [Every Agent is an API Client](https://rookery.api.me.uk/posts/every-agent-is-an-api-client/) and the latest on [good descriptions](https://rookery.api.me.uk/posts/api-descriptions-that-stand-alone/). Have a read and let Rook know what you think in the comments!
