---
author: rickymoorhouse
categories:
- Linux
comments: true
date: "2009-04-30T15:08:34Z"
link: http://blog.rickymoorhouse.co.uk/2009/04/30/linux-extend-filesystem/
slug: linux-extend-filesystem
title: 'Linux: Extend Filesystem'
wordpress_id: 1434
---

`lvextend -L +2G /dev/basevg/var_lib_mysql`




Add 2GB to the logical volume var_lib_mysql in basevg




`resize2fs /dev/basevg/var_lib_mysql`




Resize the filesystem /dev/basevg/var_lib_mysql




#### Other useful commands:


vgs

    list volume groups

lvs

    list logical volumes


