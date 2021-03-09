---
title: "API Connect Remote Gateway with IBM Cloud Satellite"
date: 2021-03-09T11:15:39Z
slug: remote-gateway-via-satellite
tags: 
 - apiconnect
 - satellite
---

## Create your Satellite location

To create a Satellite location you will need 3 hosts for the control plane, and at least one host to deploy DataPower on.  For each of the hosts you will need to do the following:

 - Set up the host prior based on the [host requirements](https://cloud.ibm.com/docs/satellite?topic=satellite-host-reqs) for Satellite.

 - Register the host for RedHat updates using `subscription-manager register` - then applying a subscription to it in the [RedHat Customer Portal](https://access.redhat.com/management/subscriptions)

 - Refresh the packages and enable the repositories
```bash
subscription-manager refresh
subscription-manager repos --enable rhel-server-rhscl-7-rpms
subscription-manager repos --enable rhel-7-server-optional-rpms
subscription-manager repos --enable rhel-7-server-rh-common-rpms
subscription-manager repos --enable rhel-7-server-supplementary-rpms
subscription-manager repos --enable rhel-7-server-extras-rpms
```

 - Run the attach script obtained from the IBM Cloud Satellite UI to attach the host.

For the three hosts to form the control plane, you will need to assign them to the Satellite control plane through the UI or CLI.

## Install DataPower in the Satellite location
 - [Download](https://www.ibm.com/support/knowledgecenter/SSMNED_v10cloud/com.ibm.apic.install.doc/ri_gw_download_install.html) the DataPower rpms from your reserved instance. 
 - [Install DataPower](https://www.ibm.com/support/knowledgecenter/SS9H2Y_10.0/com.ibm.dp.doc/virtual_forlinux.html?view=kc) on your RHEL VM.  In order to do this along with the pre-reqs I used the following commands:
```
yum install https://dl.fedoraproject.org/pub/epel/epel-release-latest-7.noarch.rpm
yum install schroot ipvsadm telnet
yum install idg_cloud1.10011.common.x86_64.rpm idg_cloud1.10011.kernel-build-tool.x86_64.rpm idg_cloud1.10011.image.x86_64.rpm
``` 

## Set up link endpoint 

 - Create a [link endpoint](https://cloud.ibm.com/docs/satellite?topic=satellite-link-location-cloud) pointing to the API Connect Gateway management endpoint (usually port 3000) 

## Configure DataPower for API Connect

 - Follow the [steps to configure your DataPower](https://cloud.ibm.com/docs/apiconnect?topic=apiconnect-ri-reg-gwy) for use with API Connect.  
 - For the certificates, in order to avoid a hostname mismatch create a self-signed keypair for the management interface for the hostname generated for your link endpoint.

## Configure Certificate Manager service

 - If you don't already have one, create a [Certificate Manager instance](https://test.cloud.ibm.com/catalog/services/certificate-manager)
 - Ensure API Connect Reserved Instance is [authorised through IAM](https://www.ibm.com/support/knowledgecenter/SSMNED_v10cloud/com.ibm.apic.install.doc/ri_gwy_certs_auth_svc.html?view=kc) to access this certificate manager instance. 

## Add Remote gateway to your reserved instance

 - [Register your gateway](https://www.ibm.com/support/knowledgecenter/SSMNED_v10cloud/com.ibm.apic.install.doc/ri_gwy_reg.html) in your API Connect Reserved Instance.
