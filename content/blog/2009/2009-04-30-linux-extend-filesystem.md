---
author: rickymoorhouse
tags:
- linux
comments: true
date: "2009-04-30T15:08:34Z"
link: https://rickymoorhouse.uk/2009/04/30/linux-extend-filesystem/
slug: linux-extend-filesystem
title: 'Linux: Extend Filesystem'
wordpress_id: 1434
atUri: "at://did:plc:r53zv4vpzeihop3aliwyejlu/site.standard.document/3mosweju23v2p"
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


