---
title: "API Connect v10 Reserved - authentication for CI/CD"
date: 2021-03-09
slug: cicd-workaround
tags: 
 - apiconnect
---

Currently the v10 Reserved Instance of API Connect doesn't yet have a simple approach for headless use of the CLI toolkit.  The following workaround details how to create a separate user in the API Manager user registry to use the toolkit in a headless environment such as a CI/CD pipeline.

<!--more-->

For interactive use of the API Connect CLI, you can login using the `--sso` option, retreive an api key with your browser and provide that to the CLI for example:

```bash
apic-slim login --server {apic-api-endpoint} --sso
```

However if you want to use the CLI in a non-interactive context such as a CI/CD pipeline you need to retrieve an IBM Cloud IAM Bearer token for the toolkit to use. This can be obtained using `ibmcloud iam oauth-tokens` and then placed in `~/.apiconnect/token` for the `apic` CLI to use.

The token file needs to contain:
```yaml
{apic-api-endpoint}/api: |
  refresh_token: ""
  access_token: {access_token} 
```

This can be done programmatically using something like this:
```bash
ibmcloud iam login --apikey {api-key}
ic iam oauth-tokens | sed 's/IAM token:  Bearer /api.9a6e-bd639816.us-south.apiconnect.cloud.ibm.com\/api: |\n  refresh_token: ""\n  access_token: /' > ~/.apiconnect/token

apic orgs --my --server {apic-api-endpoint}
production    [state: enabled]   https://api...apiconnect.cloud.ibm.com/api/orgs/9123ae60-427c-4997-8a6b-ddd75b169bfb
test-porg     [state: enabled]   https://api...apiconnect.cloud.ibm.com/api/orgs/b73708ea-a7b5-4d27-b562-80767e0b238e
```



## Invoking the API Connect REST APIs

To invoke the [API Connect REST APIs]() in Reserved Instance v10, you can use an IBM Cloud IAM token which can be obtained using the `ibmcloud iam oauth-tokens` CLI command or with an API call as detailed in the [IAM API documentation](https://cloud.ibm.com/apidocs/iam-identity-token-api#authentication).  This token can then be used as a bearer token to invoke the API Connect REST APIs.

The full process looks like this:

Firstly use your IBM Cloud API key to retrieve an IAM token

```bash
curl -X POST \
  "https://iam.cloud.ibm.com/identity/token" \
  --header 'Content-Type: application/x-www-form-urlencoded' \
  --header 'Accept: application/json' \
  --data-urlencode "grant_type=urn:ibm:params:oauth:grant-type:apikey" \
  --data-urlencode "apikey=[your api key]"

{"access_token":"[access token would be here]","refresh_token":"not_supported","token_type":"Bearer","expires_in":3600,"expiration":1615370557,"scope":"ibm openid"}
```

Then take the value of the access_token and use it to call the API Connect API e.g. 


```bash
curl https://{{ api_host }}/api/orgs \
  -H "Accept: application/json" \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer [access_token]

{
  "total_results": 2,
  "results": [
    {
      "type": "org",
      "org_type": "provider",
    ...
    }
  ]
}
```
