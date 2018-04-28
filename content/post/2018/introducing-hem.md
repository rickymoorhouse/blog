---
title: "Introducing HEM"
date: 2018-04-25
tags: []
---

<abbr title="HTTP Endpoint Monitor">HEM</abbr> is a [synthetic monitoring](https://en.wikipedia.org/wiki/Synthetic_monitoring) tool which monitors HTTP resources on a regular schedule, storing details of the time taken and the reponse code returned.

I've been using [Uptime](https://github.com/fzaninotto/uptime) at work for a while for endpoint monitoring and over the time we've been using it made a few tweaks or plugins for it - in particular being able to send metrics from Uptime to Graphite.  There were also some more substantial changes we were considering making and we'd built up a number of supporting scripts to populate the checks via the Uptime API when hosts changed.  We also have all our other monitoring dashboards in Grafana. In this context I decided that what would be nice is a simple tool that could replace the checking piece and feed that data into our graphite data store to be viewed and alerted on from Grafana. 

HEM runs from a simple config file with three main sections in it - discovery, tests and metrics.  Both discovery and metrics have been designed as pluggable to give HEM versatility - so far I've built discovery drivers for dns, consul and json/yaml and metrics drivers for graphite, kafka and the console.  HEM will iterate over the tests on a custom interval performing discovery each time to ensure it has the latest list of hosts for that test.  

![HEM stats in Grafana steps](/images/hem-grafana.png)

## Getting started with HEM

To start using HEM, you can install it from [PyPI](https://pypi.org/project/hemApp/) with pip:

    pip install hemApp

Then create a config file - it will look something like this:

        discovery:
          type: dns
        metrics:
          type: graphite
          server: 127.0.0.1
          port: 2003
        tests:
          homepage:
            path: /index.html
            secure: false
            hosts:
               - example.com
               - example.org

Run HEM and start to see metrics flowing to graphite

    hem -c config.yaml

In grafana I have the [Discrete plugin](https://grafana.com/plugins/natel-discrete-panel) installed to give the coloured bar look you see above. 
