        {{- $category := .Params.category -}}
        {{- if .Params.category -}}
        {{ else }}
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
        {{- if or (eq "microblog" .Type) (eq "flight" .Params.layout) -}}
- {{- .Date.Format "2 Jan 2006" -}}
          {{- if eq "microblog" .Type -}}
            {{- .Content -}}
              {{- with .Resources.ByType "image" -}}
                {{- range first 2 . -}}
                  {{- $image := .Fill "300x300 Center" -}}
                  ![image]({{- .Permalink -}})
                {{- end -}}
              {{- end -}}            
            {{- else if eq "flight" .Params.layout -}}
- Flight: {{- .Params.airline -}} {{- .Params.flight -}}: {{- .Params.from -}} to {{- .Params.to -}}
            {{- end -}}
        {{- else -}}
        {{- if eq "photos" .Type -}}
- {{- .Date.Format "2 Jan 2006" -}}: 
            {{- $page := . -}}
            {{- if .Resources.ByType "image" -}}
            {{- with .Resources.GetMatch .Params.featured | default (index (.Resources.ByType "image") 0) -}}
            [Photo: {{- $page.Title -}}]({{- .Permalink -}})
                {{- end -}}
              {{- end -}}
        {{- else -}}
- {{- .Date.Format "2 Jan 2006" -}}: [{{- $category | lower -}}] [{{- .Title -}}]({{- .Permalink -}})
            {{- if .Params.summary -}}
              {{- .Summary -}}
            {{- end -}}
        {{- end -}}
        {{- end -}}