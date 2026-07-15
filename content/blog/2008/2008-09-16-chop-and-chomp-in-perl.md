---
author: rickymoorhouse
categories:
- Tech
comments: true
date: "2008-09-16T10:23:28Z"
slug: chop-and-chomp-in-perl
title: Chop and chomp in perl
wordpress_id: 1445
atUri: "at://did:plc:r53zv4vpzeihop3aliwyejlu/site.standard.document/3mosweentuq23"
---

Just a reminder, so I remember the difference! - chomp is a safer version of "chop" removes any trailing string that matches what perl thinks is a new line)


`
$string = "abcdef";  
chop($string) # $s is now f, $string is now abcde  
chomp($string) # $string is still now abcde  
  
$string = "abcdefn";  
chomp($string) # $string is now abcdef  
`
