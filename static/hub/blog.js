---
layout: null
---
processContent({
"posts":[
  {% for post in site.posts  %}
    {
      "title": "{{ post.title }}",
      "url": "{{ post.url | prepend: site.baseurl | prepend: site.url }}"
    }
    {% unless forloop.last %},{% endunless %}
  {% endfor %}
]});
