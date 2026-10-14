{{- if and .File (eq .File.ContentBaseName "about") -}}
{{- /* SocialSpec profile; build.sh also copies this to /.well-known/about.md */ -}}
---
title: "About"
{{- with or (cond .Date.IsZero nil .Date) (cond .Lastmod.IsZero nil .Lastmod) }}
created_at: {{ .Format "2006-01-02T15:04:05-07:00" }}
{{- end }}
summary: {{ site.Params.description | jsonify }}
---
{{ .RenderShortcodes | strings.TrimSpace }}

## Elsewhere

{{ range site.Menus.icon -}}
- [{{ .Title }}]({{ .URL }})
{{ end -}}
{{- else -}}
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
{{ .RenderShortcodes }}


    
{{ with site.RegularPages.Related . | first 5 }}
## Related posts
{{ range . }}
- [{{ .LinkTitle }}]({{ .RelPermalink }})
{{ end }}
{{ end }}

{{ .Site.Params.copyright | default "&copy; All rights reserved." | markdownify }}
{{- end }}
