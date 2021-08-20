---
title: Debugging jobs in kubernetes
date: 2021-07-20
slug: debugging-jobs-in-k8s
tags: 
 - kubernetes
---

As jobs are often short running and finish before you can check anything within the pod, often it's helpful to make the pod run for longer to be able to inspect the environment and re-run the job manually. 
One way to do this is to extract the yaml definition for a previous run of the job and create a pod definition replacing the command with an endless sleep.

    kubectl get pod {previous-job-pod} -o yaml > pod.yaml

Then edit the pod.yaml, removing the `status` block and the additional metadata referring to the previous job so the metadata only contains name and namespace

The comand then needs to be updated/specified with something like this:

      command:
        - /bin/sh
        - '-c'
        - while true; do echo hello; sleep 10000; done

Then use `kubectl apply -f pod.yaml` to deploy the new pod definition to your cluster and you will have a long running pod with the environment and code for the job. 
