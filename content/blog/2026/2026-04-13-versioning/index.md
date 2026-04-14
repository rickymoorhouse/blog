---
title: API Versioning is a Contract Commitment, not a Technical Choice
date: 2026-04-13
layout: blog
hideImages: true
featured: windswept.jpeg
tags:
  - API
  - versioning
  - architecture
---

Teams spend a lot of energy arguing about whether to put the version in the URL, a header, or a query parameter. That debate usually misses the point. The real question is: what is your change management discipline, and how do you protect consumers from breaking changes?

![Sand in the wind, Witterings](windswept.jpeg)

Taking a step up from the versioning question - how are you managing changes to your API contract?  Ideally this would be transparent to consumers unless there is something they are looking to take advantage of in the new changes.  If your API is designed well it can abstract any internal requirements and technical limitations from your clients such that you can update the implementation internally and their applications will continue to operate without even needing to know about it.

So a versioning strategy really comes back to what sort of changes you are expecting to your API. As with most things having an understanding of what you will do in this space up front is going to make things smoother down the line.

- **Externally versioned standards** (e.g. FHIR, OpenAPI specs tied to a standard) — your hands are largely tied. Both you and your consumers need to track versions explicitly, and you'll likely need to support multiple versions in parallel during transitions.
- **Additive changes** (new fields, new endpoints) — these can often be transparent to consumers, as long as clients are told upfront to ignore unknown fields. No formal versioning strategy may be needed.
- **Breaking changes** (removing fields, restructuring data types) — you need an explicit consumer-facing versioning strategy.

You'll still need to pick an approach so here's how the main methods compare:

- **URL Path** (`/v1/`) - very common and highly visible approach, but maintaining a separate set of endpoints for every version.

- **Header-based** - keeps URLs clean, but no standard and complicates caching.

- **Query Parameters** - sitting somewhere between the two above - easy to see what is going on without multiplying endpoints for each version.

- **Gateway Managed** - instead of client specified versioning you can handle this provider side through an API Gateway, routing consumers to the version of the API they are subscribed to.

No matter which way you choose to handle changes to an API you need to start from your strategy around how you intend to handle changes to your APIs.  This needs to be an upfront plan and integrated into your API Contract commitments to your clients rather than something you leave until you need it.  Once you have a clear strategy and have committed to it, you can handle technical requirements within that framework much more easily.

When none of these options feel right or you see that breaking changes are frequent and the versioning overhead is getting in the way it may be time to look at GraphQL where you let the client determine the data they are requesting rather than dictating the content from the provider side.
