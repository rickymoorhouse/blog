---
title: Status Light
date: 2025-05-11
layout: blog
hideImages: true
tags: 
- raspberrypi
- coding
featured: robot-large.png
---

Whilst working from home it's useful for the family to know when I am on a video call or just a voice call. I was first looking at [Busy bar](https://busy.bar/preview) which I came across via [Hiro Report](http://hiro.report),  but couldn't justify the cost of it and as I had a raspberry pi zero and a [Blink!](https://shop.pimoroni.com/products/blinkt?variant=22408658695) sitting around, I decided to build something simple myself. Maybe one day I  could make it more complex and build a version using the [Pico 2 W Unicorn Galactic](https://shop.pimoroni.com/products/space-unicorns?variant=40842033561683)?

<!--more-->
![Robot with Pi Zero](robot.png#floatright)

## Hardware

- [Raspberry Pi Zero W](https://shop.pimoroni.com/products/raspberry-pi-zero-w?variant=39458414264403)
- Power Supply
- [Blink!](https://shop.pimoroni.com/products/blinkt?variant=22408658695)

## Software Part 1 - LED Control Server

This is the application that runs on the Raspberry Pi and controls the lights based on a simple API call. I deploy this to my Raspberry Pi through [Balena](https://www.balena.io/) for ease of management and updates - then I can just push a new copy of the code into git and balena will automatically deploy it to my Raspberry Pi.

The API Call is very simple and currently accepts a GET request with parameters for the red, green and blue values (between 0 and 255) - really this should probably be a PUT request but using GET made testing with a browser simpler.  The light is switched off with a DELETE call (or another GET with 0 for each parameter).

You can see the code for this in the `light` directory.

## Software Part 2 - Webcam detection tool


This part runs on my laptop and detects when the webcam is in use through monitoring the system log - if a change in state is detected, it then sends an API call to the Raspberry Pi to switch the light on or off as appropriate.

The tricky part here was the detection of the webcam - I found a few different samples and a useful reddit thread (which I can't find now - will add the link later!) on ways to detect the webcam being operational on MacOS and it seems it is liable to change between MacOS versions - looking for eventMessages containing `AVCaptureSessionDidStartRunningNotification`, `AVCaptureSessionDidStopRunningNotification` or `stopRunning` seems to work for the things I've tested on Sequoia. 

The alternative route I was considering was to use [OverSight](https://github.com/objective-see/OverSight) to trigger a CLI app and leave the detection to them - but having the CLI detect it was more interesting to build. 

You can see the code for this part in the `cli` directory. 

The code for this project lives at [github.com/rickymoorhouse/status-light](https://github.com/rickymoorhouse/status-light/).

