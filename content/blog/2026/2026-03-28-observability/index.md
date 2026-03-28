---
title: Observability as a design requirement
date: 2026-03-28
layout: blog
hideImages: true
featured: lighthouse.jpg
summary: Observability is a design decision, not an afterthought. From the platform team to API consumers to AI agents, knowing what is happening across your API — and building that in from the start — is what gives you confidence when things go wrong in production.
tags:
  - architecture
  - api
---

## What can you actually see in your API platform?


To go from an API working for the developer building it to knowing it is working for your consumers is where API observability is key and can give you the confidence in the decisions you made building it. 

I once made the mistake of turning off logging of metrics for one of our APIs and only discovered this when we needed to debug an issue, at which point we were blind to what was happening with it.  As well as having a strategy for observability, it's important to check it is working as expected!

![Lismore Lighthouse](lighthouse.jpg)

## What do your error responses tell the consumer?

The API Consumer needs visibility too, not the same view as those running the platform but enough to figure out if their calls are successful and when they're not why. Status codes and error responses are the primary way to do this and providing something clear and actionable makes it a lot easier for consumers to self-resolve issues. 

Beyond the API response itself it is also key to give them a way to see how their applications are calling the API once they are deployed and probably can't see the response directly. This is often through the developer portal so they can easily find out how their applications are using the APIs alongside the documentation and credential management. 

Clear actionable responses and observability is even more crucial when the consumer is an AI agent. An agent won't infer what's going on from an obscure error code and outdated documentation. It will retry and seek to workaround the problem likely in ways you didn't intend.  For agent consumers, having clear and actionable errors are the difference between recovering gracefully and getting stuck in a runaway loop.

## Correlation and trace propagation as contract commitments

If you're committed to providing this traceability of requests to your API, why not include the appropriate headers in your OpenAPI specification as part of the contract. This makes it clear for the consumer this is something the API provides you rather than there being mysterious extra headers on requests that you don't know if you can rely on to use. If it makes sense to and is possible then supporting propagation of trace headers from inbound requests makes sense - in multi-region distributed systems these can be really valuable in understanding what is happening.


## Designing for debuggability, not just availability

As you build out your API architecture, ask yourself: "how will I know what is happening here?" If you can answer that at design time, you'll have it covered when you need it in production.

The time to think about what you'd need to debug a problem is when you're designing the system — not at 3am when you're already in the middle of a failure.

A consistent, unique request ID propagated through all your logs and traces is one of the simplest things you can do. When something goes wrong, being able to follow a single transaction end-to-end across your system is invaluable.


---

Observability isn't something that you bolt on after your API is live - it is worth thinking through as you design your system.  A well thought out strategy here will save you and your consumers time in production.