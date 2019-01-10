let map;
let markers = [];
const button = document.getElementById('map-button');
const latlng = document.getElementById('latlng');

function initMap() {
  map = new google.maps.Map(document.getElementById('map'), {
    center: {lat: 51.500149, lng: -0.126240},
    zoom:12
  });

  map.addListener('click', function(event) {
    for (let m of markers) {
      m.setMap(null);
    }

    marker = new google.maps.Marker({
      position: event.latLng,
      map: map
    });

    markers = []
    markers.push(marker)


    let lat = event.latLng.lat().toString()
    let lng = event.latLng.lng().toString()
    latlng.value = lat + ',' + lng

    button.disabled = false
  });
}
