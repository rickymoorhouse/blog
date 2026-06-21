---
author: rickymoorhouse
tags:
- linux
- tech
comments: true
date: "2009-04-27T12:50:43Z"
link: https://rickymoorhouse.uk/2009/04/27/linux-what-is-using-up-disk-space/
slug: linux-what-is-using-up-disk-space
title: 'Linux: What is using up disk space?'
wordpress_id: 1435
atUri: "at://did:plc:r53zv4vpzeihop3aliwyejlu/site.standard.document/3moswejxbvf2f"
---

`du -m | sort -nr | head`






du -m

    summarises disk usage from current path recursively (in megabytes)

sort -nr
    sorts the output numerically in reverse

head
    restricts output to the top 10 lines




adapted from [Linux Reviews](http://linuxreviews.org/quicktips/chkdirsizes/)

