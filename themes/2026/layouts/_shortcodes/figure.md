{{- /* Markdown version of Hugo's built-in figure shortcode */ -}}
{{- $src := .Get "src" -}}
{{- $url := $src | absURL -}}
{{- if not (or (hasPrefix $src "/") (strings.Contains $src "://")) }}{{ $url = printf "%s%s" $.Page.Permalink $src }}{{ end -}}
{{- with $.Page.Resources.GetMatch $src }}{{ $url = .Permalink }}{{ end -}}
{{- $alt := .Get "alt" | default (.Get "title") | default (.Get "caption") | default "" -}}
![{{ $alt }}]({{ $url }})
{{- with .Get "caption" }}{{ if ne . $alt }}
*{{ . | plainify }}*{{ end }}{{ end -}}
