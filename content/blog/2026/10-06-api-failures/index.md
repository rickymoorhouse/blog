---
title: "API failure stories and what they taught me"
date: 2026-10-06T21:25:00+01:00
publishDate: 2026-08-22

layout: blog
category: technical
tags:
  - api
summary: "Four anonymised API failure stories about versioning, migration testing, sensitive data, and authorisation, with practical lessons for preventing them."
featured: "DSC_0086.jpeg"
hideImages: true
---

API failures often come from missing lifecycle controls rather than difficult technology. These generalised stories from my experience show how unchecked assumptions around versioning, testing, logging, and access control can create avoidable problems.

<!--more-->

## When API versions stop making sense

Imagine an API with versions like these: 

`v1`, `v1-updated`, `v2`, `v2-legacy`, `v3-final`, `v3-final-final`

The problem isn't that multiple versions exist. Supporting multiple versions in parallel is a common, deliberate and reasonable decision. The problem here is missing lifecycle controls to define how versions would be created and retired - each time the API was changed the versioning approach had to be reinvented alongside the change. This results in no one knowing:

- which versions are in use
- which consumers are using which ones
- which versions can be safely retired
- what would break if one of them was turned off. 

This also made consumer-reported issues harder to diagnose: before debugging could begin, the team first had to establish which API version the consumer was using.

Up front you need to define a [versioning](/blog/2026/api-versioning-is-a-contract-commitment-not-a-technical-choice/) and deprecation strategy - it needs to cover how breaking changes are identified, how long older ones remain supported and how consumers will migrate. [Structured usage data](/blog/2026/observability-as-a-design-requirement/) is also essential as you need to know which consumers are still actively using a version before you can safely retire it.

## A migration without reusable tests

A migration was planned - same software but a different environment and with it new network routing. The migration itself was straightforward, but the lack of reusable tests made it a lengthy manual comparison exercise. This consisted of calling each API in turn with curl on the new and old environments, then painstakingly comparing the responses and headers  - each subtle difference discussed and examined - will this cause a problem anywhere?

The migration exposed differences in how network paths and forwarding headers were handled. Some consumers behaved differently in the new environment as the pre-cutover manual testing didn't cover every consumer behaviour.

Testing needs to be considered an ongoing exercise and even if you find yourself coming up to a change without tests, building them for re-use based on the existing traffic rather than as a one-off migration exercise will bring benefits. AI tooling can assist with comparisons generating initial tests and sample calls, but the resulting tests still need to be reviewed against the contract and the intended behaviour and maintained over time.

## Sensitive data in the wrong places

Operational reviews can surface sensitive data in places it shouldn’t be. The discovery then triggers an incident response process, which then has to establish how the data had arrived, where else it had been stored, and how it could be removed. This then can lead to identifying other places where sensitive data wasn't being handled as intended in the implementation.

Solving this properly is something that needs to start in your API design - make sure you have a good understanding of all the sensitive data your APIs will be touching and how it will be handled. Then build up a layered approach to protect it:

- API design: sensitive data should never be logged in plaintext, so shouldn't appear in the query string - if needed for a query then do this through a POST body but make sure you have no logging of body content.
- Redaction: configure redaction policies for fields containing sensitive data to keep them out of logs
- Log levels: ensure the logging levels you have don't log request and response body
- Environmental configurations: sometimes you may need to see how data is handled in dev, but restrict when it goes to UAT or preprod - apply this at the environment level.

Any per API setting needs to be checked in your pipeline and used as a gate - then your development debugging never accidentally makes it to production. For a deeper look at implementing these controls in API Connect, see [Securing Sensitive Payload Logging in API Connect](/blog/2026/securing-sensitive-payload-logging-in-api-connect/).



## Authenticated does not mean authorised

This first came to me in a quiet conversation - "I think we found a bug in the portal", but turned out to be a misconfiguration based on false assumptions. The portal used OIDC-based SSO through an identity provider that allowed self-registration. Authentication was working, but no authorisation controls had been configured - once you were in you could see, subscribe and call any API - they were effectively public to anyone who could self-register with the provider.

Fortunately in this instance, no one had exploited the misconfiguration before it was caught and corrected.

Whilst some APIs may have been intended for a wide public audience, the majority weren't. The solution here is granular controls ensuring you control who can discover the API exists (visibility) and who can subscribe to it (subscribability). For APIs that need more control, make use of explicit approval flows so access to the individual API becomes the control point. The key thing to remember here is that we need both authentication (who someone is) and authorisation (what they may do).

---

In each case, the technology was capable of doing the right thing. The problem was that an assumption had not been turned into a documented rule, an automated test, or an enforced control.

Next time, before releasing or changing an API, ask:

- Do we know how breaking changes will be versioned and deprecated?
- Do we know which consumers use each version?
- Can we repeat the tests that validate the API’s expected behaviour?
- Have we identified sensitive data and prevented it from reaching logs or query strings?
- Have we verified we have both authentication and authorisation configured appropriately?
- Are these expectations enforced in the delivery pipeline rather than just relying on people remembering?
