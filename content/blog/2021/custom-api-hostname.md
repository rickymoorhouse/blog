---
link: https://community.ibm.com/community/user/integration/blogs/ricky-moorhouse1/2021/05/28/customising-the-api-invocation-hostname-in-v10-res
title: Customising the API invocation hostname in v10 Reserved Instance 
date: 2021-05-28
category: technical
atUri: "at://did:plc:r53zv4vpzeihop3aliwyejlu/site.standard.document/3moswe6x72j2p"
---

Once you have your APIs ready to be used but before sharing them with developers if is often key to have them served on your own hostname rather than the built in hostnames that come out of the box with reserved instance.  For Reserved Instance v10 you can now manage the hostname used for API Calls yourself through the IBM Cloud console without needing to open a support case.

## Configure Certificate Manager Service

- If you don’t already have one, create a Certificate Manager instance
- Ensure API Connect Reserved Instance is authorised through IAM to access this certificate manager instance.
- Upload a certificate and private key for DataPower to present for your hostname to your certificate manager instance

## Configure the SNI mapping for the gateway

- Open your Reserved instance customisation interface from the top-level item from the API Connect services list with the plan of ‘Reserved’
- Select 'Gateways' and then click on the name of the gateway service you wish to configure the hostname against.
- Select your certificate manager service from the drop down
- Add the desired domain to the “Domains handled by gateway via SNI” section and select the certificate you uploaded and select Save.
![Domains handled via SNI screenshot](https://higherlogicdownload.s3.amazonaws.com/IMWUC/UploadedImages/810b57c9-2b5c-4d73-af24-03e4f679ef41/Domains_handled_by_gateway_via_SNI.png)

## Ensure your DNS routes traffic to the gateway

The way you do this will differ, depending on your DNS provider, but you will need to create a CNAME record for the new hostname pointing to the hostname displayed under ‘Base URL of API invocation endpoint’ above the SNI mapping list.

## Update your catalog to display the new hostname

- Open the API Manager view for the provider org you wish to update and select ‘Manage Catalogs’
- Select the catalog you wish to update, ‘Catalog settings’, ‘API endpoints’ and then Edit.
- Tick the box entitled ‘Display vanity endpoint’, select ‘Catalog priority’ and then add the new hostname to the list of base endpoints and click Save:



