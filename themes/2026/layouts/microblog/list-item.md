- {{- .Date.Format "2 Jan 2006" -}}
{{- .Content -}}
{{- with .Resources.ByType "image" -}}
  {{- range first 2 . -}}
    {{- $image := .Fill "300x300 Center" -}}
    ![image]({{- .Permalink -}})
  {{- end -}}
{{- end -}}
