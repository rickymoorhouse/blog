---
author: rickymoorhouse
categories:
- Tech
comments: true
date: "2008-09-16T10:23:28Z"
link: https://rickymoorhouse.uk/2008/09/16/chop-and-chomp-in-perl/
slug: chop-and-chomp-in-perl
title: Chop and chomp in perl
wordpress_id: 1445
---

Just a reminder, so I remember the difference! - chomp is a safer version of "chop" removes any trailing string that matches what perl thinks is a new line)


`
$string = "abcdef";  
chop($string) # $s is now f, $string is now abcde  
chomp($string) # $string is still now abcde  
  
$string = "abcdefn";  
chomp($string) # $string is now abcdef  
`
