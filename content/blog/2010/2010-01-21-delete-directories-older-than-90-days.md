---
author: rickymoorhouse
categories:
- Linux
- tech
comments: true
date: "2010-01-21T10:25:16Z"
link: https://rickymoorhouse.uk/2010/01/21/delete-directories-older-than-90-days/
slug: delete-directories-older-than-90-days
title: Delete directories older than 90 days
wordpress_id: 1394
---

`
find /var/log/hostdb/* -type d -mtime +90 -exec rm -rf {} ;
`



-type d
    only look at directories, f would be files
-mtime +90
    modified time greater than 90 days ago
