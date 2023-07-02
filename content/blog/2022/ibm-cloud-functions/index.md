---
link: https://community.ibm.com/community/user/integration/blogs/ricky-moorhouse1/2022/10/04/invoke-ibm-cloud-functions-from-api-connect?CommunityKey=2106cca0-a9f9-45c6-9b28-01a28f4ce947
title: "Invoke IBM Cloud Functions from API Connect"
date: 2022-10-25
description: Originally posted on the IBM Integration Community Blog
slug: ibm-cloud-functions
tags:
 - apiconnect
 - serverless
---

[Cloud functions](https://cloud.ibm.com/functions/learn/concepts) offer an easy way to build functionality and only pay for the time they are actually running  without having to worry about how it will be hosted - you just right the code, save it and it is ready to be invoked. The function can be invoked through an event trigger or as a REST API - in this case I'm going to show how you can trigger a function as part of your API Connect assembly flow - providing an easy way to manage and socialise the functionality you have built.

To call an IBM Cloud function you first need to exchange your IBM Cloud API Key for an IAM access key using the [IAM Authentication API](https://cloud.ibm.com/apidocs/iam-identity-token-api#authentication).  

This is a case of setting up and sending a post request to IBM Cloud IAM, to do this I used a set-variable policy to configure the headers and body followed by an invoke to https://iam.cloud.ibm.com/identity/token. The set-variable looks like this:

```yaml
      - set-variable:
          version: 2.0.0
          title: setup iam request
          actions:
            - set: message.headers.content-type
              value: application/x-www-form-urlencoded
              type: string
            - set: message.headers.accept
              value: application/json
              type: string
            - set: message.body
              type: string
              value: >-
                grant_type=urn:ibm:params:oauth:grant-type:apikey&apikey=$(iam-apikey)​
```

Once you have this access key you can use this to call your function using the endpoint provided in the UI:


{{{<diagram example-function.png >}}

For the authentication to the function URL we need to set the Authorization header to `Bearer {access_key}` where access_key is from the body of the previous request, so to obtain this we can use a Parse policy to parse the returned json, and then another set-variable policy to configure the headers for the Function invoke. This time the set-variable looks like this:

```yaml
      - set-variable:
          version: 2.0.0
          title: setup function call
          actions:
            - set: message.headers.authorization
              value: Bearer $(iam.body.access_token)
              type: string
            - set: message.body
              value: $(request.body)
              type: any
            - set: message.headers.accept
              value: application/json
              type: string
```
As you can see we're setting the authorization and accept headers, and passing the original request body from the inbound request.  We follow this with an invoke of the function URL and a map, because the JSON returned from the function API includes details on invocation as well as the defined response:

{{{<diagram "map.png" >}}

The end to end flow looks like this:

{{{<diagram "end-to-end-flow.png" >}}

Here is the [complete sample swagger file](https://gist.github.com/rickymoorhouse/95ca5237bf93f31c2d1629b94662882d)  which can be used in any API Connect deployment, including our new [API Connect service on AWS](https://register.automation.ibm.com/apic/trial/aws?source=blog_2022-10-25)