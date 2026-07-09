# {{ .Title }}

{{ .Content }} {{/* This renders any text you put in _index.md */}}

{{/* Filter for both posts and micro content */}}
{{ $stream := where .Site.RegularPages "Section" "in" site.Params.MainSections }}
    

{{ range $stream.ByDate.Reverse }}
{{ partial "short-list-item-md" . }}
{{ end }}
