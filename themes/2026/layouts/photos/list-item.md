- {{- .Date.Format "2 Jan 2006" -}}:
{{- with .Resources.GetMatch .Params.featured | default (index (.Resources.ByType "image") 0) -}}
  [Photo: {{- $.Title -}}]({{- .Permalink -}})
{{- end -}}
