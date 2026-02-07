(function () {
    'use strict';

    // Your additional js should go there

}());

function insertMap(geojson_url) {
  var currentTheme = document.documentElement.getAttribute('data-theme') || 
                    (window.matchMedia("(prefers-color-scheme: dark)").matches ? 'dark' : 'light');
  var mapStyle = currentTheme === 'dark' ? 'mapbox://styles/mapbox/dark-v10' : 'mapbox://styles/mapbox/light-v9';
  
  var map = new mapboxgl.Map({
      container: 'map', // container id
      style: mapStyle, //'mapbox://styles/rickymoorhouse/cih6ouins00f3bnm500a1d3dl',
      center: [-53, 20], // starting position
      zoom: 1.5 // starting zoom
  });
  
  // Listen for theme changes
  var themeObserver = new MutationObserver(function(mutations) {
    mutations.forEach(function(mutation) {
      if (mutation.attributeName === 'data-theme') {
        var theme = document.documentElement.getAttribute('data-theme');
        if (theme) {
          var newStyle = theme === 'dark' ? 'mapbox://styles/mapbox/dark-v10' : 'mapbox://styles/mapbox/light-v9';
          if (map.getStyle() !== newStyle) {
            map.setStyle(newStyle);
          }
        }
      }
    });
  });
  themeObserver.observe(document.documentElement, { attributes: true });
  
  map.on('load', function() {
    map.addSource("visited", {
      type: 'geojson',
      data: geojson_url
    });
    map.addLayer({
       "id": "points",
       "type": "symbol",
       "source": "visited",
       "layout": {
           "icon-image": "star-11",
           //"text-field": "{name}",
           "text-font": ["Open Sans Semibold", "Arial Unicode MS Bold"],
           "text-offset": [0, 0.6],
           "text-anchor": "top"
       }
     });
  });
}
