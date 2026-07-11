---
link: https://community.ibm.com/community/user/integration/blogs/ricky-moorhouse1/2021/07/01/avoid-delays-from-validate-compilation-in-api-defi
title: Avoid delays from validate compilation in your APIs 
date: 2021-07-01
category: technical
atUri: "at://did:plc:r53zv4vpzeihop3aliwyejlu/site.standard.document/3moswe6tzka2e"
---

When re-publishing an API with validation steps in it, you may well see that the first call to the API experiences higher latency than subsequent calls. This is due to the following as [described in the documentation](https://www.ibm.com/docs/en/datapower-gateways/10.0.x?topic=definitions-configuring-api-schema):

>Schemas are compiled before they are used for validation. Because the compilation process is longer than the validation process, the compiled schema artifacts are stored in a cache. The limited capacity of the cache can cause older entries to be evicted from the cache when newer entries are added. Schemas whose artifacts have been evicted from the cache must be recompiled, which can cause significant delays in validation. You can specify the capacity of the stylesheet cache in the API Gateway.

In order to avoid your API Consumers hitting this delay in their applications you can trigger this to be pre-compiled as part of your CI/CD pipeline. If you add an an additional path to your API definition that only does the validate stage of the API this allows you to trigger the compilation without running the full API. This can be then called as part of your CI/CD pipeline against each gateway in the environment after the API is published to ensure that the validation step is compiled as soon as possible to avoid your API consumers hitting the delay.

I’ve also found it useful to have this validation path return some of the context variables to assist with debugging so you can confirm the version and id of the API matches that published and you haven’t hit the previous version due to any timing issues - a pipeline could compare these ids with the one published or prior to publish, but that is out of scope for this article.

An example path implementation such as the following referencing your existing definition:

```yaml
 - condition: ($operationPath() = '/validate')
   execute:
     - parse:
         version: 2.0.0
         title: parse
         parse-settings-reference:
           default: apic-default-parsesettings
         input: message
         output: ''
         use-content-type: true
     - validate:
         version: 2.0.0
         title: validate
         input: message
         validate-against: definition
         definition: '#/definitions/simpleObject'
         output: ''
         description: Test validation policy
     - set-variable:
         version: 2.0.0
         title: set-variable
         actions:
           - set: message.body
             value: >-
               {"validated":"$(session.localAddress)","api_id":"$(api.id)","api_version":"$(api.version)"}
             type: string
```

If you are running gateways in kubenetes, you normally won’t be able to target the pods independently from outside of the environment. This can be worked around by creating a separate API that will be used to invoke the validate path on your API for you against the internal pod hostnames - you just need to add an invoke step for each gateway pod - using the internal hostnames of the form: {pod-name}.{service-name}.{namespace}.svc

For example in v2018:

    r6d0b871026-dynamic-gateway-service-0.r6d0b871026-dynamic-gateway-service.apic.svc

Or in v10: 

    gateway-0.gateway-datapower-all.apic.svc

You could then use a map in this API to consolidate the responses from each gateway for assistance with any debugging.

See a full example of an [API calling across each gateways](https://gist.github.com/rickymoorhouse/ca40eedda469c0791b6804da45412c4a).
