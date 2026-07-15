---
author: rickymoorhouse
categories:
- Linux
comments: true
date: "2007-08-30T23:00:00Z"
slug: watching-log-files-for-something
title: Watching log files for something
wordpress_id: 1483
atUri: "at://did:plc:r53zv4vpzeihop3aliwyejlu/site.standard.document/3moswelaprv2p"
---

Found from: [techblog](http://blog.nominet.org.uk/tech/2005/05/26/tail-f-with-highlighting/):



`
tail -f /var/log/apache2/access_log | sed "s/rss/Ctrl+vCtrl+[[41;1mrssCtrl+vCtrl+[[0m/g"
`


This example is looking for people accessing the rss feed so I can see how frequently it gets hit (whilst still seeing what else is going on).  With this I spotted that one of the Firefox extensions I was using([piclens](http://piclens.com)) was automatically downloading the detected rss feed with every page access. It's a nice extension and I can see why it does that, but I don't want to be accessing rss feeds automatically and potentially multiple times as I use sites.
