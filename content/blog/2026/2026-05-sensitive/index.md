---
title: Securing Sensitive Payload Logging in API Connect
date: 2026-05-22
layout: blog
hideImages: true
bsky: 3mmllf5p5jc2h
summary: Overview of ways to handle sensitive data payloads within API Connect and controlling where that data ends up.
tags:
 - apiconnect
 - security
atUri: "at://did:plc:r53zv4vpzeihop3aliwyejlu/site.standard.document/3mos64z2ty22s"
---

Unintentionally logging sensitive customer data (PII, financial info) is a major compliance risk. When deploying APIs, ensuring that this data is kept out of your logs requires robust, layered controls. Whilst developing APIs that will deal with this sensitive content you will often need to see what is being passed to ensure that everything is being handled as expected. Very often in a development or test environment you will be using a dummy payload to ensure the API is working as expected so it is key to ensure it is reflected at the different stages of processing as part of your test suites.

When you progress to partner integration testing with an API you are no longer as in control of the payload passed in through the client, so at this point become dependent on payload logging to see what is being passed and processed. At this point as we would still be dealing with dummy data this would be acceptable in most cases.

Once the API use progresses towards production and real sensitive data is being transferred you need safeguards in place to ensure the data is no longer being logged. Of course data security requires a layered approach and this article only covers one area of this - payload controls.  This needs to be paired with additional strong security controls such as ensuring there is encryption in transit and at rest across your system and sensitive data isn't being transmitted in the query string which could be logged by other network components ([owasp ref](https://owasp.org/www-community/vulnerabilities/Information_exposure_through_query_strings_in_url)).

In API Connect there are several features that can be used to assist with this and the combination to use will be different depending on your specific requirements.  Depending on your goal will determine which one is most appropriate in your scenario:

- To see the data in lower environments to assist in development, make use of full payload activity logging
- Protect specific fields in logs using redaction policies
- Ensure compliance standards are met across the board make use of Governance Rulesets
- To prevent any logging of certain data globally, make use of analytics Filters

Let's examine each of these features in turn:

## Activity Log settings

The default behaviour in API Connect is to log activity for all APIs and only log payload (request and response body) on error - but this can be customised on a per-API basis. For the DataPower API Gateway, this is configured in the [activity-log](https://www.ibm.com/docs/en/api-connect/cloud/12.1.0?topic=policies-activity-log) extension and the options are payload, activity, headers or none and in the yaml it looks something like this:

```yaml
activity-log:
  success-content: headers
  error-content: headers
  enabled: true
```

This could also be configured to reference Catalog properties so that you make these settings at a catalog level and all the APIs reference this with syntax like `$(catalog-error-content)` in your api definition.

## Redaction policy for field level controls

If you don't want to restrict the entire body of the API and it is specific known fields that contain sensitive data, you can use the redaction policy to remove or replace these fields with asterisks. The policy uses JSONata to identify the fields to modify.  For this you need to first use the log policy in gather-only mode in order to modify the logging. The `gather-only` mode in the log policy is crucial because it instructs the policy to collect the full, sensitive payload and place it into the internal log context object. This allows the subsequent redact policy to operate on the logging data itself, prior to it being written to analytics, ensuring the client receives an unmodified response while the sensitive data is masked in the logs.

```yaml
- log:
  title: Gather log to redact
  version: 2.0.0
  mode: gather-only
- redact:
    version: 2.0.0
    title: redact birthday in the logged data
    redactions:
      - action: redact
        path: $.**.birthday"
    root: log.response_body
```

Whilst this can also be used to remove or redact the full body it is more typically used on individual fields as adding a policy to each API when you can just set the activity log level is mostly overkill.

## Governance rulesets to check

Whichever approach you take, you can make use of governance rulesets to ensure that all APIs meet your standards - these can be used in a CI CD pipeline for checking the status before publish or even configured on a catalog to block publish if the rules aren't met. Governance within API Connect supports the use of spectral rulesets to scan API specifications at development time, through CI/CD pipelines and in periodic catalog scans.

```yaml
extends: spectral:oas

rules:
  # Ensure activity-log.success-content is header
  activity-log-success-content-header:
    description: "activity-log.success-content must be set to 'header'"
    message: "activity-log.success-content must be 'header'"
    severity: error
    given: $.x-ibm-configuration.activity-log
    then:
      field: success-content
      function: pattern
      functionOptions:
        match: "^header$"

  # Ensure activity-log.error-content is header
  activity-log-error-content-header:
    description: "activity-log.error-content must be set to 'header'"
    message: "activity-log.error-content must be 'header'"
    severity: error
    given: $.x-ibm-configuration.activity-log
    then:
      field: error-content
      function: pattern
      functionOptions:
        match: "^header$"

```

## Analytics filters

If you need to ensure these are never logged in the whole API Connect deployment you can set up filters in the Analytics Cluster configuration.  There are two settings here one for storage and one for offload. 

```yaml
spec:
  ...  
  ingestion:
    ...
    filter: |
      mutate {
        remove_field => ["response_body"]
      }
```

Navigating payload security in API Connect is not about choosing one feature; it's about implementing a defense-in-depth strategy. Start with foundational security (encryption in transit and at rest). Then, apply appropriate Activity Log configuration to get appropriate visibility at each stage. Where you need more fine-grained control, use Redaction Policies to target specific fields. 

To continuously validate your configurations meet your compliance requirements make use of governance rulesets in CI/CD and finally, use Analytics Filters as a system-wide preventative guardrail. By stacking these tools appropriately you move from merely tracking data to actively securing it throughout its entire lifecycle. 