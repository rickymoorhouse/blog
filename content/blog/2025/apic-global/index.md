---
outputs: [html]
layout: blog
title: Global Deployment with API Connect
date: 2025-07-12
hideImages: true
draft: true
---


If you have customers around the world you might want to serve them from a global API Connect footprint such that they can call the API from a location closest to them. 

In this example I'm deploying my APIs to the 6 current regions of the API Connect Multi-tenant SaaS service on AWS. At the time of writing these are N. Virginia, Frankfurt, London, Sydney, Mumbai and Jakarta. I will use N. Virginia as the initial source location.

![API Connect Global Deployment](map.png)

## Automatically Deploy APIs and Products to all locations

Create a pipeline that deploys APIs and products to all regions - you could base this around the [sample github action available](https://github.com/ibm-apiconnect/actions) or build it using the [example CLI scripts](https://github.com/ibm-apiconnect/devops). This then will enable me to 

![Pipeline](pipeline.png)

## Create an API Connect instance in each region

Create an API Connect instance in each of the regions you want to deploy to. You can use the same image as your source location, but make sure to specify a different hostname for each instance. Each paid subscription for API Connect SaaS includes up to 3 instances which can be distributed as you wish across the available regions.

## Configure the portal for the source location

In my simple example I opted to use the new [Consumer Catalog](https://consumer-catalog.us-east-a.apiconnect.automation.ibm.com/ibm/production) as I don't need to configure any custom branding or anything like that. However I did enable approval flows for sign ups so that I can manage who has access to my APIs and products.

![Portal](portal.png)

## Configure ConfigSync to push configuration changes to all regions

As config sync runs from a source to a target region, you need to run it for each target region in turn. In my case this is done with a loop through the hostnames and a lookup for the appropriate API Key to use for each region.

![Config Sync](configsync.png)

The script I'm using looks like this:

```bash
#!/bin/bash

# US East is always the source catalog
export SOURCE_ORG=ibm
export SOURCE_CATALOG=production
export SOURCE_REALM=provider/default-idp-2
export SOURCE_TOOLKIT_CREDENTIALS_CLIENTID=599b7aef-8841-4ee2-88a0-84d49c4d6ff2
export SOURCE_TOOLKIT_CREDENTIALS_CLIENTSECRET=0ea28423-e73b-47d4-b40e-ddb45c48bb0c

export SOURCE_MGMT_SERVER=https://platform-api.us-east-a.apiconnect.automation.ibm.com/api
export SOURCE_ADMIN_APIKEY=$(grep 'us-east-a\:' ~/.apikeys.cfg | awk '{print $2}')


# Set common properties for all targets - in SaaS the toolkit credentials are common across regions.
export TARGET_ORG=ibm
export TARGET_CATALOG=production
export TARGET_REALM=provider/default-idp-2
export TARGET_TOOLKIT_CREDENTIALS_CLIENTID=599b7aef-8841-4ee2-88a0-84d49c4d6ff2
export TARGET_TOOLKIT_CREDENTIALS_CLIENTSECRET=0ea28423-e73b-47d4-b40e-ddb45c48bb0c

# Loop through the other regions to use as sync targets
stacklist="eu-west-a eu-central-a ap-south-a ap-southeast-a ap-southeast-b"
for stack in $stacklist 
do
    export TARGET_MGMT_SERVER=https://platform-api.$stack.apiconnect.automation.ibm.com/api
    export TARGET_ADMIN_APIKEY=$(grep "$stack\:" ~/.apikeys.cfg | awk '{print $2}')
    ./apic-configsync
done
```

For handling the API Keys for each region I have a file `~/.apikeys.cfg` in which each line contains a pair of values in the form `region: apikey`

## Verify that everything works as expected

- In the source region, register a consumer org in the portal and subscribe to a product that contains an API to use.
- Use the "Try now" section to invoke the API
- Ensure the configsync job has had time to complete successfully for each region
- Call the same API across the other regions to validate that everything is working as expected.

## Possible next steps

- Configure global load balancing to route customers to the closest location automatically. 