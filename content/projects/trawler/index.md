---
title: Trawler
date: 2020-06-02
layout: project
description: Metric gathering for API Connect
technology: Go, Kubernetes, Prometheus, Grafana
tags:
- trawler
featured: trawler-grafana.png
---

Trawler is a metric gathering tool for IBM API Connect deployments, built to monitor Kubernetes-based API Connect cloud deployments.

It runs alongside API Connect in Kubernetes and identifies API Connect components, exposing metrics to Prometheus or other compatible monitoring tooling. The data feeds into dashboards such as Grafana for visualization.

## Metrics Collected

### Management Subsystem
- API Connect version information (apiconnect_build_info)
- User and organization counts (users, provider_orgs, consumer_orgs)
- Catalog and product/API counts

### DataPower Subsystem
- TCP connection stats
- Log target stats (events processed, dropped, pending)
- Object counts (SSLClientProfile, APICollection, etc.)
- HTTP statistics

### Analytics Subsystem
- Cluster health status
- Node and shard counts
- Pending tasks

## Related Blog Posts

{{< tagged-posts "trawler" >}}
