---
Title: "{{ .Name | replaceRE `[-_]+` ` ` | title }}"
date: {{ dateFormat "2006-01-02" .Date }}
lat: 
lng: 
tags: [photos]
Images:
  - src: ""
---

