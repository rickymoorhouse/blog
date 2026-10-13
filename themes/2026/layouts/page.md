---
title: {{ .Title | jsonify }}
description: {{ .Description | default .Summary | plainify | jsonify }}
date: {{ .Date.Format "2006-01-02T15:04:05Z07:00" }}
updated: {{ .Lastmod.Format "2006-01-02T15:04:05Z07:00" }} 
author: "Ricky Moorhouse"
tags: {{ .Params.tags | jsonify }}
canonical: "{{ .Permalink }}"
---
# {{ .Title }}
{{ .RawContent }}


    
{{ with site.RegularPages.Related . | first 5 }}
## Related posts
{{ range . }}
- [{{ .LinkTitle }}]({{ .RelPermalink }})
{{ end }}
{{ end }}

{{ .Site.Params.copyright | default "&copy; All rights reserved." | markdownify }}
