---
title: Everything as code
date: 2026-07-19
layout: blog
category: technical
featured: IMG_0559.jpeg
hideImages: true
tags:
  - apiconnect
  - gitops
  - iac
---

A valuable technique I've found is treating everything I can as code - checked in, reviewed, and versioned. This post covers what that looks like across infrastructure, deployments, APIs, and even documentation, and why the discipline matters more than any specific tool.

![Coffee roasting](IMG_0559.jpeg)


## What does "as code" mean?

By 'as code' I mean storing as a version controlled source of truth in a declarative form. This is distinct from building custom code as an automation in that what is being stored represents the desired state, not the steps to get there.

## What can be treated as code?


- **Infrastructure**:  defining the infrastructure components and configuration through a declarative language to be used with a tool such as [Terraform](https://www.hashicorp.com/en/products/terraform) to deploy and maintain state.
- **Application deployments**: for deployments to Kubernetes, you can use YAML manifests in a repository and then [ArgoCD](https://argo-cd.readthedocs.io/en/stable/) will keep the cluster in sync with what you have defined.
- **API definitions**: Store your OpenAPI specifications and gateway policy definitions in version control and use the API Connect toolkit to publish them to your gateway and developer portal - [example with GitHub Actions](https://github.com/rickymoorhouse/api-automation/blob/main/.github/workflows/deploy-api.yaml).
- **Governance rulesets**: See also [Git is your governance source of truth](https://apievangelist.com/2026/06/30/git-is-your-governance-source-of-truth/)
- **Process documentation & runbooks**: Storing your documentation and runbooks as [markdown](https://daringfireball.net/projects/markdown/) in a repo gives you that built in change history and management rather than having to remember to update the changelog manually in the front of a word document.
- **Diagrams**: If you make use of a text based diagramming tool such as [Mermaid](https://mermaid.ai/), you can get these same benefits for your architecture diagrams making it easier to see over time how things have changed. Whilst you could also store [draw.io diagrams](https://www.drawio.com) in git and follow the changes, it is slightly less clear with its XML-based format.

## Advantages

- Traceability — you know who made which changes.
- Currency — you know when it was last updated.
- Time travel — git history lets you revisit any prior state.
- Repeatable and Consistent — you can always instantiate from the declarative source
- Peer review via PRs — there is a built in system for proposing and reviewing changes
- Drift detection — you can see when your system diverges from the source

## How this works in practice

This model is fundamental to how my team at IBM works. All our internal documentation and runbooks live as markdown files in git repos. For our cloud deployments the infrastructure is defined in Terraform, all the manifests are stored in git and deployed with ArgoCD. Having this consistency and repeatability is essential when you're maintaining over 80 stacks. We deploy a set of our own APIs to every stack using the toolkit. My next post will cover more detail on our deployments.

## Pitfalls to watch

Whilst treating everything as code has its advantages there are a number of things to watch out for. You need to make sure you have a way to handle sensitive data separately and ideally scanning to avoid these being unintentionally leaked through your version control system.
Not all data types work well in a system designed around text files, for example large or binary data that you can't easily compare changes in. This will balloon the repo size and start to make things painful for everyone using it.
The review process can become tedious if not handled carefully - it needs to be thought through so that you get the benefit of peer review without it becoming a checkbox or a blocker.

## Conclusion

The value in treating everything as code really comes from the mindset and the discipline around it, which is much more powerful than any specific tool. If you adopt this approach you get a common set of consistent practices across many different artifacts: traceability, review and a way to revert changes. In my next post I'll dig into how this is done in our API Connect cloud deployments.
