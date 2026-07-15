---
author: rickymoorhouse
tags:
- linux
comments: true
date: "2008-04-24T12:08:20Z"
slug: extending-a-logical-volume-using-reiserfs
title: Extending a logical volume using reiserfs
wordpress_id: 1460
atUri: "at://did:plc:r53zv4vpzeihop3aliwyejlu/site.standard.document/3moswefkd5n2f"
---

Just recording this so I can find it again!


`
    **nandu:~ #** lvextend -L +2G _/dev/basevg/opt_  

  

      Extending logical volume opt to 5.00 GB  

      Logical volume opt successfully resized  

  

    **nandu:~ #** resize_reiserfs _/dev/basevg/opt_  

  

    resize_reiserfs 3.6.19 (2003 www.namesys.com)  

    resize_reiserfs: On-line resizing finished successfully.  

  

    **nandu:~ #**  

`
