var map = L.map('map').setView([48.8566, 2.3522], 13); // Paris par défaut

L.tileLayer('https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png', {
    attribution: '&copy; <a href="https://www.openstreetmap.org/copyright">OpenStreetMap</a> contributors'
}).addTo(map);

var marker;

// Fonction pour envoyer des coordonnées au serveur backend
function sendCoordinatesToServer(lat, lng) {
    axios.post('/api/parking/search', { lat: lat, lng: lng })
        .then(function(response) {
            console.log('Parking locations received:', response.data);
            // Ici, vous pouvez traiter la réponse et ajouter des marqueurs rouges sur la carte
        })
        .catch(function(error) {
            console.error('Error fetching parking locations:', error);
        });
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
                marker = L.marker([coords[1], coords[0]]).addTo(map)
                    .bindPopup('Votre position')
                    .openPopup();

                // Envoyer les coordonnées au serveur après conversion d'adresse
                sendCoordinatesToServer(coords[1], coords[0]);
            } else {
                alert("Adresse non trouvée.");
            }
        })
        .catch(function (error) {
            console.log(error);
        });
});

document.getElementById('submitCoordinates').addEventListener('click', function() {
    var coordsInput = document.getElementById('coordinates').value.split(',');
    var lat = parseFloat(coordsInput[0].trim());
    var lng = parseFloat(coordsInput[1].trim());

    if (!isNaN(lat) && !isNaN(lng)) {
        map.setView([lat, lng], 13);
        if (marker) {
            map.removeLayer(marker);
        }
        marker = L.marker([lat, lng]).addTo(map)
            .bindPopup('Votre position')
            .openPopup();

        // Envoyer directement les coordonnées au serveur
        sendCoordinatesToServer(lat, lng);
    } else {
        alert("Coordonnées invalides.");
    }
});
