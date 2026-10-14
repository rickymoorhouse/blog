{{- $tag := .Get 0 -}}
{{- $limit := .Get 1 -}}
{{- $wanted := lower $tag -}}
{{- $pages := slice -}}
{{- range where site.RegularPages "Section" "in" "blog" -}}
  {{- $tags := slice -}}
  {{- range (default slice .Params.tags) }}{{ $tags = $tags | append (lower .) }}{{ end -}}
  {{- if in $tags $wanted }}{{ $pages = $pages | append . }}{{ end -}}
{{- end -}}
{{- with $limit }}{{ $pages = first (int .) $pages }}{{ end -}}
{{- if $pages -}}
{{- range $pages }}
- [{{ .Title }}]({{ .Permalink }}) - {{ .Date.Format "2 Jan 2006" }}
{{- end -}}
{{- else -}}
No blog posts tagged **{{ $tag }}** yet.
{{- end -}}
