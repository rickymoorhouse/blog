---
title: "Raspberry Pi Weather Station"
date: 2018-05-12
slug: weather-station
tags:
 - raspberry pi
 - weather
---

For a while I've been meaning to write up the details of the Raspberry Pi weather station that I have built with my eldest daughter.  This project builds on a number of examples I've seen across the internet, particularly [sensing the weather](https://www.raspberrypi.org/learning/sensing-the-weather/). This details how our system is put together.

### Temperature monitoring

We took two temperature sensors and mounted them in a garden post with one pushed down to the bottom for soil temperature and one in the cap for the air temperature.  The one-wire sensors can share the same three wires, so are both connected to a wire leading back to the Raspberry Pi through a hole drilled into the side of the post.  For waterproofing we surrounded the whole with hot glue. The post is situated in a shady spot and pushed about 30 centimeters deep in the soil. 

### Wind speed



You can see my [graphs of the data](/weather), and the [code is on github](https://github.com/rickymoorhouse/weather).

