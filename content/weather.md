---
layout: page
title: Weather
---

<iframe src="https://rickymoorhouse.uk/grafana/d-solo/ZjaRJ0TZz/weatherweb?orgId=1&panelId=2&theme=light" width="750" height="400" frameborder="0"></iframe>
<iframe src="https://rickymoorhouse.uk/grafana/d-solo/ZjaRJ0TZz/weatherweb?orgId=1&panelId=5&theme=light" width="750" height="400" frameborder="0"></iframe>

<script type="text/javascript">
function activateDarkMode() {
  jQuery('iframe').each(function (i, e) {
    e.src = e.src.replace('light','dark');
  })
}
function activateDarkMode() {
  jQuery('iframe').each(function (i, e) {
    e.src = e.src.replace('dark','light');
  })
}
function setColorScheme() {
  const isDarkMode = window.matchMedia("(prefers-color-scheme: dark)").matches
  const isLightMode = window.matchMedia("(prefers-color-scheme: light)").matches
  const isNotSpecified = window.matchMedia("(prefers-color-scheme: no-preference)").matches
  const hasNoSupport = !isDarkMode && !isLightMode && !isNotSpecified;
  if (isDarkMode) {
    activateDarkMode()
  }
  window.matchMedia("(prefers-color-scheme: dark)").addListener(e => e.matches && activateDarkMode())
  window.matchMedia("(prefers-color-scheme: light)").addListener(e => e.matches && activateLightMode())
}
</script>
