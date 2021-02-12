class Location {
  constructor(name, position, file) {
    this.name = name;
    this.pos = position;
    this.filePath = file;
  }

  fetchData(pointsLayer) {
    return new Promise((resolve, reject) => {
      let layer = L.markerClusterGroup({ removeOutsideVisibleBounds: true, disableClusteringAtZoom: 15, spiderfyOnMaxZoom: false });
      fetch(this.filePath)
        .then(response => response.text())
        .then(data => {
          let lines = data.split('\n');
          lines.splice(0, 1);
          lines.forEach(element => {
            try {
              if (element != '') {
                let s = element.split(',')
                if (s[0] == 'Point') {
                  let c = L.circle({ lat: parseFloat(s[1]), lon: parseFloat(s[2]) }, 10, { color: '#0000FF', opacity: 1 });
                  c.addTo(pointsLayer);
                } else {
                  let c = L.circle({ lat: parseFloat(s[1]), lon: parseFloat(s[2]) }, 20, { color: '#FF0000', opacity: 1, title: s[0] });
                  c.bindTooltip(s[0]);
                  c.addTo(layer);
                }
              }
            } catch (error) {
              resolve(null);
            }
          });
          resolve({ layer: layer, location: this });
        }).catch((e) => {
          resolve(null);
        })
    });
  }
}
