---
title: "API Connect v10 Reserved - workaround for CI/CD"
date: 2021-03-09
slug: cicd-workaround
tags: 
 - apiconnect
---

Currently the v10 Reserved Instance of API Connect doesn't yet have a simple approach for headless use of the CLI toolkit.  The following workaround details how to create a separate user in the API Manager user registry to use the toolkit in a headless environment such as a CI/CD pipeline.

<!--more-->
Firsly download appropriate toolkit for your stack and login specifying the using manager endpoint (credential download has api. - replace with manager.) and `--sso`

```bash
apic-slim --server manager.{your-stack} --sso
```

Once you have the toolkit set up and configured using the SSO login, we will use this to create an invitation in order to add the new user.
Create the invitation yaml file, calling it `invite.yaml` with the following contents:

```yaml
email: {your-email}
```

Run the following command to create the invitaton.  Using `--debug` will show the activation link in the output, avoiding the need to retreive the link from your e-mail:

```bash
apic-slim --server manager.{your-stack} member-invitations:create --scope org --org {your-org} invite.yaml --debug
```

Open the activation link in your browser, and sign up using API Manager User Registry to create your user for CI/CD use

