---
title: "Adding SocialSpec to my site"
date: 2026-10-18
layout: blog
category: work
tags:
  - blog
  - socialspec
  - hugo
hideImages: true
---

On Tuesday, Caleb Hailey [announced](https://calebhailey.com/links/socialspec/) [SocialSpec](https://socialspec.org) around the premise that the future of social media is websites. This maps out a consistent way to expose key social data (about, contact, following) from your website based around existing standards and ways things are typically done already. This makes it very easy to adopt and add to an existing website - for me this meant the following:

## Start with a feed

I'd previously ended up with my feeds available at multiple URLs so this was an opportunity to clean things up. Rather than just copying what I had to the feed.xml and feed.json locations and add more complexity, I decided to make these the definitive sources for my feed and redirected the old URLs to them through edge rules. To get [Hugo](https://gohugo.io) to create an RSS feed in another location to the default index.xml (which I'd never liked), I created a custom output format [for RSS](https://github.com/rickymoorhouse/blog/blob/main/themes/2026/layouts/home.feedxml.xml) and referenced this in the config. I already had a custom output format for jsonfeed as Hugo doesn't have that built in. My custom output references my adapted rss.xml, but you could just point to the built-in one. The config.yaml looks like this:

```yaml
outputFormats:
  feedxml:
    mediaType: "application/rss+xml"
    baseName: "feed"
    rel: "alternate"
    noUgly: true
  feedjson:
    mediaType: "application/feed+json"
    baseName: "feed"
    rel: "alternate"
    isPlainText: true
outputs:
  home: ["HTML", "FEEDXML", "FEEDJSON"]
```

## About Page - [aboutspec.org](https://aboutspec.org)

I updated my blog build process to copy my markdown about page into the .well-known folder:

```sh
cp public/about/index.md public/.well-known/about.md
```

## Contact Me - [contactspec.org](https://contactspec.org)

I exported a vCard (.vcf) and updated it to just have the values I wanted to share. I then dropped this in my static/.well-known/ folder and updated my CDN settings in Bunny to serve it as text/vcard based on the file extension. This works as an Edge Rule where if the RequestURL matches *.vcf, then it sets a response header.

## Following - [followspec.org](https://followspec.org)

Initially I was just going to export an OPML file from [NetNewsWire](https://netnewswire.com/), but I decided to create a [data file](https://github.com/rickymoorhouse/blog/blob/main/data/blogroll.yaml) for the blog so Hugo would generate both an OPML file to put in .well-known as well as an HTML [blogroll](https://rickymoorhouse.uk/blogroll) which will hopefully make both easier to update going forward. Again this needed a CDN update for the content type to text/x-opml.

## Testing this

After adding these I explored testing them through [HyperTexting](https://hypertexting.com/), Caleb's social news feed based on the existing connections across the open web - an ungated social network. As this didn't work I built my own [test tool](https://rickymoorhouse.uk/socialspec) with Claude to validate what I had set up against the spec. After contacting Caleb, it [turned out](https://socialspec.org/news/hypertexting/#fn:1) the version available at the time wasn't yet using the full spec but rather an earlier iteration - but on the TestFlight version of the update it worked perfectly. For now I have added a temporary edge rule to redirect the hypertexting specific URLs.

This is early days for the spec but looks to be a good way to make social connections more open.
