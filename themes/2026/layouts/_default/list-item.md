{{- $category := .Params.category -}}
{{- if not $category -}}
  {{- if eq "photos" .Type -}}{{- $category = "Visual" -}}
  {{- else if in .Params.tags "apiconnect" -}}{{- $category = "Technical" -}}
  {{- else if in .Params.tags "walk" -}}{{- $category = "Personal" -}}
  {{- else if in .Params.tags "work" -}}{{- $category = "Work" -}}
  {{- else if in .Params.tags "photography" -}}{{- $category = "Personal" -}}
  {{- else if in .Params.tags "coding" -}}{{- $category = "Technical" -}}
  {{- else if in .Params.tags "travel" -}}{{- $category = "Travel" -}}
  {{- else if eq .Type "projects" -}}{{- $category = "Technical" -}}
  {{- end -}}
{{- end -}}
- {{- .Date.Format "2 Jan 2006" -}}: [{{- $category | lower -}}] [{{- .Title -}}]({{- .Permalink -}})
{{- if .Params.summary -}}
  {{- .Summary -}}
{{- end -}}
