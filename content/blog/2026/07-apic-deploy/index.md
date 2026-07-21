---

title: GitOps Deployment of API Connect
date: 2026-07-18
tags:

- apiconnect

---

As architect for the API Connect Cloud offerings one of the key areas I am involved in is deployment and in particular deployment automation.  With my SRE background the main goal here is that anything we need to do more than once should be automated - deployment being a big one of these.  Across our cloud environments - single-tenant and multi-tenant, IBM Cloud, AWS and Azure from dev through to production we probably have over 80 deployments of API Connect.  These all use automation to deploy from declarative deployment models - in particular GitOps so our git repo is the source of truth for everything that gets deployed.

This is split into two primary areas - deployment of cloud services dependencies (Kubernetes clusters, object storage set up etc. ) and the application deployment itself.

## Infrastructure - Terraform

For the cloud service deployments we use Terraform so we can declaratively describe the infrastructure requirements and have clean separation between the base template and the per environment configuration (region, size, ha-requirements) through variables. This all lives in git.

## Application - ArgoCD

For everything that goes into kubernetes we use ArgoCD - which means all of the manifests for deployment live in our git repos and are watched by ArgoCD for changes. These are structured making use of ArgoCD's SyncWaves so that they are deployed in the right order and we know that the dependencies are in place before moving on. For example:

- -200 - Pre-requisites (cert-manager & issuers)
- -100 - Monitoring tooling
- 300 - API Connect CRDs and operators
- 400 - Management subsystem
- 500 - Analytics subsystem
- 600 - Developer portal
- 700 - Gateways

Just like in the old days of basic we've used multiples of 100 to allow us to add things in between later without reshuffling everything! In ArgoCD the default syncwave for anything without one specified is zero - so using negative waves for pre-reqs means we don't have to annotate all the CRDs and if we miss anything we know the pre-reqs are already there.  In the manifests this would look like:

```yaml
metadata:
  annotations:
    argocd.argoproj.io/sync-wave: "100"
```

This is a simplified overview, in our SaaS environments we add additional cloud specific components that handle tenant provisioning and ui based configuration addons which have their own waves in the deployments. We follow a similar pattern with the manifests that we do with the terraform - a base template and environment specific configuration.  In this case we have used kustomize & helm based charts in different places as they both have distinct benefits for different use cases.

**Use Kustomize** when environments have significant differences. It uses a base template and overlays, making it much easier to follow what is actually happening compared to complex Helm syntax.

**Use Helm** when environments are identical except for minor elements (like hostnames). It uses values files to pass variables into charts, making it perfect for simple toggles (e.g., dev vs. prod).

In a repo the difference looks like this:

<div class="two-col">

<div>

#### Kustomize

```text

bases/
    management/
        management_cr.yaml
        kustomization.yaml
    gateway/
        gateway_cr.yaml
        kustomization.yaml
    overlays/
        dev/
            kustomization.yaml
            management-patch.yaml
            gateway-patch.yaml
        prod/
            kustomization.yaml
            management-patch.yaml
            gateway-patch.yaml
```

</div>

<div>

#### Helm

```text
Chart.yaml
values.yaml
values-dev.yaml
values-prod.yaml
templates/
    management_cr.yaml
    gateway_cr.yaml
```

</div>

</div>

With Kustomize the `bases/management/management_cr.yaml` holds the common shape of the `ManagementCluster` CR and `overlays/dev/management-patch.yaml` only contains the fields that differ for that environment (endpoint hostnames, [profiles](https://www.ibm.com/docs/en/api-connect/software/12.1.1?topic=profiles-component-cpu-limits-memory-limits-licensing), feature enablement). The patch only carries the fields that differ for this environment:

```yaml
# overlays/prod/management-patch.yaml
apiVersion: management.apiconnect.ibm.com/v1beta1
kind: ManagementCluster
metadata:
  name: management
  namespace: apic-prod
spec:
  profile: n3xc4.m16
  endpoints:
    management: mgmt.prod.example.com
```

The `overlays/dev/kustomization.yaml` then pulls it all together:

```yaml
apiVersion: kustomize.config.k8s.io/v1beta1
kind: Kustomization
resources:
  - ../../bases/management
  - ../../bases/gateway
patchesStrategicMerge:
  - management-patch.yaml
  - gateway-patch.yaml
```

With Helm the same effect comes from templating the differing fields in `templates/management_cr.yaml` and overriding them per environment in the values file:

```yaml
# values-prod.yaml
management:
  profile: n3xc4.m16
  endpoints:
    management: mgmt.prod.example.com
```

We use Helm for our multi-tenant SaaS environments where the regional deployments need to be the same and Kustomize for single tenant deployments where we need to support more per-tenant differences.

## Secrets

Everything that is not sensitive lives in the git repo - the secrets are then injected into the charts at deploy time from the relevant secrets manager for the cloud provider.  These are abstract primarily through the use of [ArgoCD Vault Plugin](https://argocd-vault-plugin.readthedocs.io/en/stable/) which supports a number of different secret backends. 

This means our secret manifests have references rather than the actual secrets. For example the `Secret` we mount for the Management subsystem's DB credentials in prod looks like this:

```yaml
apiVersion: v1
kind: Secret
metadata:
  name: mgmt-admin-pass
  namespace: apic
type: Opaque
stringData:
  password: <path:apiconnect/prod/management#db.password>
```

At sync time ArgoCD Vault Plugin resolves each `<path:...#...>` reference against the configured secret backend (IBM Cloud Secrets Manager, HashiCorp Vault, AWS Secrets Manager etc.) and rewrites the manifest with the literal values before it is applied to the cluster - the rendered manifest never lands in git, and the cluster ends up with a standard `Secret` that the operator can consume.

For customer owned secrets we've [integrated](https://www.ibm.com/docs/en/api-connect/cloud/12.1.1_saas?topic=domain-managing-external-secrets-datapower-nano-gateway) [External Secrets Operator](https://external-secrets.io/latest/) to provide a similar abstraction at runtime.
