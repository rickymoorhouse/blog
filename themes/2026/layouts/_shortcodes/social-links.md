{{- with site.Menus.icon -}}
{{- range sort . }}
- [{{ with .Params.title }}{{ . }}{{ else }}{{ with .Title }}{{ . }}{{ else }}{{ .Name | humanize | title }}{{ end }}{{ end }}]({{ .URL }})
{{- end -}}
{{- end -}}
