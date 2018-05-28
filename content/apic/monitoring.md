---
layout: page
title: Monitoring API Connect
---

## Monitoring Metrics

We've standardised on [Grafana](https://grafana.org/) for viewing metric data via dashboards and sending alerts to PagerDuty and Slack - here's a rough list of the different types of data we're monitoring. The majority of these are collected via [collectd](https://collectd.org/) and stored in [graphite](http://graphite.readthedocs.io/en/latest/), although some of the dashboards will use data directly from our [Elasticsearch](https://elastic.co) logging infrastructure.

### System Metrics 

Standard system metrics collected by collectd from the individual VMs and push to graphite 

 - CPU usage
 - Network utilisation
    - Socket states (e.g. count of established, are processes listening)
    - Transfer rate
 - Memory usage 
   - system overall
   - process size (e.g. datapower)
 - Disk usage
 - Load


### Product Metrics

#### API Invocation 
 - Transactions per second [ Count of ExtLatency logs from datapower ] <sup>l</sup>
 - Rate of errors (for stable APIs) [ Analysis of response codes from branding ] <sup>l</sup>

#### Analytics 

##### Ingestion of Analytics Events 
 - Error level for inbound data to Analytics <sup>l</sup>
 - WSM Agent lost record count from DataPower <sup>cs</sup>

##### Health of Analytics Cluster
 - Cluster health <sup>cs</sup>
 - Shard Counts <sup>cs</sup>
 - Pending Tasks <sup>cs</sup>

#### API Manager
 - Apache connection levels <sup>cp</sup>

#### Informix
 - Tablespace usage <sup>cs</sup>


#### Overall Product usage

Internal REST endpoints used to regularly generate reports for data such as

 - Number of provider orgs
 - Number of API definitions
 - Policy usage



### Externals
 - Synthetic monitoring - response status and times using [Hem](https://rickymoorhouse.co.uk/post/introducing-hem/) and [Uptime](https://github.com/fzaninotto/uptime)
    - Sample APIs - [echo](https://api.us.apiconnect.ibmcloud.com/api-connect-ops/live/public/echo?text=monitoring), [proxy](https://api.us.apiconnect.ibmcloud.com/api-connect-ops/live/public/proxy), etc.
    - Product APIs - LB Healthcheck, v1/me/orgs



### Key to data sources:


 - <sup>cs</sup> - CollectD custom script
 - <sup>cp</sup> - CollectD plugin
 - <sup>l</sup> - Log analysis in ELK



## Log Analysis

We use [ELK](https://elastic.co) as our centralised logging infrastructure with all of our systems offloading logs via syslog.

The logs are parsed and indexed by logstash on the way into the cluster.  Everything gets indexed, and some patterns are identified to raise PagerDuty alerts.

Some examples of patterns we're using to alert on include:

 - Higher than normal rate of 502 or 503 errors in the Analytics inbound logs
 - Errors for known error states - e.g. out of memory and database conditions.

