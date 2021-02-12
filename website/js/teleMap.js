var map = L.map('map', { preferCanvas: true, layers: [] }).setView(locations[0].pos, zoom);

L.tileLayer('https://{s}.tile.openstreetmap.fr/hot/{z}/{x}/{y}.png', {
  maxZoom: 19,
  attribution: '&copy; <a href="https://openstreetmap.org/copyright">OpenStreetMap contributors</a>'
}).addTo(map);
var searchControl = new L.Control.Search({ layer: new L.layerGroup(), hideMarkerOnCollapse: true, marker: { circle: { color: '#00FF00', radius: 2 }, icon: false, animate: false }, zoom: 17 });
map.addControl(searchControl);

var pointsLayer = L.layerGroup();
const promises = [];
locations.forEach((location) => {
  promises.push(location.fetchData(pointsLayer));
});

var userMaps = {};
var overlayMaps = { "Stations": pointsLayer }
Promise.all(promises)
  .then((results) => {
    var first = true;
    for (let i = 0; i < results.length; i++) {
      if (results[i]) {
        if (first) {
          first = false;
          map.panTo(results[i].location.pos, zoom);
          results[i].layer.addTo(map)
          searchControl.setLayer(results[i].layer);
        }

        userMaps[results[i].location.name] = results[i].layer;
      }
    }

    //pointsLayer.addTo(map);
    map.addControl(L.control.layers(userMaps, overlayMaps, { position: "bottomleft" }));
  });

map.on('baselayerchange', function (e) {
  locations.forEach((loc) => {
    if (e.name == loc.name)
      map.setView(loc.pos, zoom);
  });
  searchControl.setLayer(e.layer);
});
