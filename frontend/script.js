var map = L.map('map').setView([48.8566, 2.3522], 13);
 
L.tileLayer('https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png', {
    attribution: '&copy; <a href="https://www.openstreetmap.org/copyright">OpenStreetMap</a> contributors'
}).addTo(map);
 
var marker;
 
function addMarker(lat, lon, message, color = 'blue') {
    var newMarker = L.marker([lat, lon], {icon: new L.Icon({iconUrl: `https://raw.githubusercontent.com/pointhi/leaflet-color-markers/master/img/marker-icon-${color}.png`, iconSize: [25, 41], iconAnchor: [12, 41], popupAnchor: [1, -34], shadowSize: [41, 41]})});
    newMarker.addTo(map).bindPopup(message);
    return newMarker;
}
 
function reverseGeocode(lat, lon, capacity) {
    var geocodeURL = `https://nominatim.openstreetmap.org/reverse?format=json&lat=${lat}&lon=${lon}`;
 
    fetch(geocodeURL)
        .then(response => response.json())
        .then(data => {
            var address = data.display_name ? data.display_name : "Adresse non trouvée";
            var message = `Capacité: ${capacity}<br>Adresse: ${address}`;
            addMarker(lat, lon, message, 'red');
        })
        .catch(error => console.error('Error:', error));
}
 
document.getElementById('submitAddress').addEventListener('click', function() {
    var address = document.getElementById('address').value;
    var photonAPI = "https://photon.komoot.io/api/?q=" + encodeURIComponent(address);
 
    axios.get(photonAPI)
        .then(function (response) {
            if(response.data.features.length > 0) {
                var coords = response.data.features[0].geometry.coordinates;
                map.setView([coords[1], coords[0]], 13);
                if (marker) {
                    map.removeLayer(marker);
                }
                marker = addMarker(coords[1], coords[0], 'Votre position', 'blue');
                searchAndDisplayParking(coords[1], coords[0]);
            } else {
                alert("Address not found.");
            }
        })
        .catch(function (error) {
            console.error(error);
        });
});
 
document.getElementById('submitCoordinates').addEventListener('click', function() {
    var coordsInput = document.getElementById('coordinates').value.split(',');
    var lat = parseFloat(coordsInput[0].trim());
    var lon = parseFloat(coordsInput[1].trim());
    map.setView([lat, lon], 13);
    if (marker) {
        map.removeLayer(marker);
    }
    marker = addMarker(lat, lon, 'Votre position', 'blue');
    searchAndDisplayParking(lat, lon);
});
 
function searchAndDisplayParking(lat, lon) {
    fetch(`http://localhost:5000/api/parking/search?lat=${lat}&lon=${lon}`)
        .then(response => response.json())
        .then(data => {
            data.forEach(parking => {
                reverseGeocode(parseFloat(parking.lat), parseFloat(parking.lon), parking.capacity);
            });
        })
        .catch(error => console.error('Error:', error));
}