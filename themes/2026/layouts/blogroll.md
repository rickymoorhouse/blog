---
title: {{ .Title | jsonify }}
description: {{ .Description | plainify | jsonify }}
author: {{ site.Params.author | jsonify }}
canonical: "{{ .Permalink }}"
---
# {{ .Title }}

{{ .RenderShortcodes | strings.TrimSpace }}
{{ range partial "blogroll/groups.html" . }}
{{ with .name }}
## {{ . }}
{{ end }}
{{ range .feeds -}}
- [{{ .title }}]({{ .htmlUrl | default .xmlUrl }}) ([RSS]({{ .xmlUrl }})){{ with .description }}: {{ . }}{{ end }}
{{ end -}}
{{ else }}
Coming soon: I'm still gathering the list.
{{ end }}
[Download as OPML]({{ "/.well-known/following.opml" | absURL }})
