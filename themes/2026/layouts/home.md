# {{ .Site.Params.title }}
{{ .Site.Params.description }}

## Featured posts

{{ $featured := where (where site.RegularPages "Type" "in" site.Params.mainSections) "Params.sticky" "==" true -}}
  {{- if $featured -}}
      {{- range $featured -}}
        {{- $page := . -}}
- [{{ $page.Title }}]({{ .Permalink }}) - {{ $page.Date.Format "2 January 2006" }}
{{ end -}}
  {{- end }}

## Recent Posts

{{ range first 5 (where site.RegularPages "Type" "in" site.Params.mainSections) -}}
- {{ .Date.Format "2 Jan 2006" }} - [{{ .Title }}]({{ .Permalink }})
{{ end }}

[View all posts](/stream/)

{{ if .Site.Menus.icon -}}
{{- range sort .Site.Menus.icon -}}
- [{{ .Name }}]({{ .URL }})
{{ end -}}
{{- end }}

{{ .Site.Params.copyright | default "&copy; All rights reserved." | markdownify }}
