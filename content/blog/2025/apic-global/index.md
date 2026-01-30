---
outputs: [html]
layout: blog
tags:
 - apiconnect
 - global
title: Global Deployment with API Connect - Serving APIs Worldwide
date: 2025-09-17
hideImages: true
sticky: true
---

## Why Global API Deployment Matters

If you have customers around the world, serving your APIs from a global footprint significantly improves their experience by reducing latency and increasing reliability. With API Connect's multi-region capabilities, you can ensure users call your APIs from locations closest to them, providing faster response times and better resilience against regional outages.

In this guide, I'll walk through deploying APIs to the 6 current regions of the API Connect Multi-tenant SaaS service on AWS. At the time of writing, these regions are:
- North America: N. Virginia
- Europe: Frankfurt, London
- Asia-Pacific: Sydney, Mumbai, Jakarta

I'll use N. Virginia as the initial source location and demonstrate how to synchronize configuration across all regions.

![API Connect Global Deployment](map.png)

## Automatically Deploy APIs and Products to all locations

To maintain consistency across regions, you'll need a reliable deployment pipeline. This pipeline should handle the deployment of APIs and products to all regions whenever changes are made to your source code repository.

You can build this pipeline using either:
- The [sample GitHub Action workflow](https://github.com/ibm-apiconnect/actions) provided by IBM
- Custom scripts based on the [example CLI scripts](https://github.com/ibm-apiconnect/devops) in the devops repository

This automation ensures that whenever you merge changes to your main branch, your APIs and products are consistently deployed across all regions without manual intervention.

![Pipeline Architecture](pipeline.png)

## Create an API Connect instance in each region

Before configuring your global deployment, you'll need to:

1. Create an API Connect instance in each target region
2. Use the same configuration as your source location (N. Virginia in this example)
3. Specify a unique hostname for each regional instance

**Pro Tip:** Each paid subscription for API Connect SaaS includes up to 3 instances which can be distributed across the available regions as needed. For a truly global footprint covering all 6 regions, you'll need two subscriptions.

## Configure the portal for the source location

For developer engagement, you'll need a portal where API consumers can discover and subscribe to your APIs. In my implementation, I chose the new [Consumer Catalog](https://consumer-catalog.us-east-a.apiconnect.automation.ibm.com/ibm/production) for its simplicity and ease of setup.

While I didn't need custom branding for this example, I did enable approval workflows for sign-ups. This allows me to:
- Review all registration requests
- Control access to sensitive APIs
- Manage who can subscribe to which products

![Portal Configuration](portal.png)

## Configure ConfigSync to push configuration changes to all regions

The key to maintaining consistency across regions is ConfigSync, which pushes configuration changes from your source region to all target regions. Since ConfigSync operates on a source-to-target basis, you'll need to run it for each target region individually.

My implementation uses a bash script that:
1. Sets the source region (N. Virginia)
2. Defines common properties for all target regions
3. Loops through each target region, setting region-specific properties
4. Runs the ConfigSync tool for each region

![Config Sync Architecture](configsync.png)

Here's the script I use:

```bash
#!/bin/bash

# US East is always the source catalog
export SOURCE_ORG=ibm
export SOURCE_CATALOG=production
export SOURCE_REALM=provider/default-idp-2
export SOURCE_TOOLKIT_CREDENTIALS_CLIENTID=599b7aef-8841-4ee2-88a0-84d49c4d6ff2
export SOURCE_TOOLKIT_CREDENTIALS_CLIENTSECRET=0ea28423-e73b-47d4-b40e-ddb45c48bb0c

# Set the management server URL and retrieve the API key for the source region
export SOURCE_MGMT_SERVER=https://platform-api.us-east-a.apiconnect.automation.ibm.com/api
export SOURCE_ADMIN_APIKEY=$(grep 'us-east-a\:' ~/.apikeys.cfg | awk '{print $2}')


# Set common properties for all targets - in SaaS the toolkit credentials are common across regions.
export TARGET_ORG=ibm
export TARGET_CATALOG=production
export TARGET_REALM=provider/default-idp-2
export TARGET_TOOLKIT_CREDENTIALS_CLIENTID=599b7aef-8841-4ee2-88a0-84d49c4d6ff2
export TARGET_TOOLKIT_CREDENTIALS_CLIENTSECRET=0ea28423-e73b-47d4-b40e-ddb45c48bb0c

# Loop through the other regions to use as sync targets
# Format: eu-west-a (London), eu-central-a (Frankfurt), ap-south-a (Mumbai), 
# ap-southeast-a (Sydney), ap-southeast-b (Jakarta)
stacklist="eu-west-a eu-central-a ap-south-a ap-southeast-a ap-southeast-b"
for stack in $stacklist 
do
    # Set the target management server URL for the current region
    export TARGET_MGMT_SERVER=https://platform-api.$stack.apiconnect.automation.ibm.com/api
    # Retrieve the API key for the current region from the config file
    export TARGET_ADMIN_APIKEY=$(grep "$stack\:" ~/.apikeys.cfg | awk '{print $2}')
    # Run the ConfigSync tool to synchronize configuration from source to target
    ./apic-configsync
done
```

For managing API keys, I store them in a configuration file at `~/.apikeys.cfg` where each line contains a region-key pair in the format `region: apikey`. This approach keeps sensitive credentials out of the script itself - for a more production ready version this api key handling would be handed off to a secret manager.

## Verify that everything works as expected

After setting up your global deployment, it's crucial to verify that everything works correctly across all regions. Follow these steps:

1. **Test the source region first:**
   - Register a consumer organization in the portal
   - Subscribe to a product containing an API you want to test
   - Use the "Try now" feature to invoke the API and verify it works

2. **Verify ConfigSync completion:**
   - Check logs to ensure the ConfigSync job has completed successfully for each region
   - Verify that all configuration changes have been properly synchronized

3. **Test each target region:**
   - Call the same API from each region using the appropriate regional endpoint
   - Verify that response times, behavior, and results are consistent
   - Check analytics to confirm that traffic is being properly recorded in each region

4. **Monitor for any issues:**
   - Watch for any synchronization failures or configuration discrepancies
   - Address any region-specific issues that might arise

## Possible next steps

Once your global API deployment is working, consider these enhancements:

- **Implement global load balancing** to automatically route customers to the closest region based on their location
- **Set up cross-region monitoring** to track performance and availability across all regions
- **Implement disaster recovery procedures** to handle regional outages gracefully

## Conclusion

A global API deployment strategy with API Connect provides significant benefits for organizations with worldwide customers. By following the approach outlined in this guide, you can:

- Reduce latency for API consumers regardless of their location
- Improve reliability through geographic redundancy
- Maintain consistent configuration across all regions
- Simplify management through automation

While setting up a global footprint requires some initial configuration, the long-term benefits for your API consumers make it well worth the effort.
