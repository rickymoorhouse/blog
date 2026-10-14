{{- with $.Page.Resources.GetMatch (.Get 0) -}}
{{- $alt := "" -}}
{{- if reflect.IsImageResourceWithMeta . }}{{ with .Meta }}{{ with .Exif }}{{ $alt = .ImageDescription }}{{ end }}{{ end }}{{ end -}}
![{{ $alt | strings.TrimSpace }}]({{ .Permalink }})
{{- end -}}
