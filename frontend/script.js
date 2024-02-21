var map = L.map('map').setView([48.8566, 2.3522], 13); // Paris par défaut

L.tileLayer('https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png', {
    attribution: '&copy; <a href="https://www.openstreetmap.org/copyright">OpenStreetMap</a> contributors'
}).addTo(map);

var marker;

document.getElementById('submitAddress').addEventListener('click', function() {
    var address = document.getElementById('address').value;
    var photonAPI = "https://photon.komoot.io/api/?q=" + encodeURIComponent(address);

    axios.get(photonAPI)
        .then(function (response) {
            if(response.data.features.length > 0) {
                var coords = response.data.features[0].geometry.coordinates;
                var nominatimAPI = `https://nominatim.openstreetmap.org/reverse?format=json&lat=${coords[1]}&lon=${coords[0]}&zoom=18&addressdetails=1`;

                axios.get(nominatimAPI).then(function(nominatimResponse) {
                    var addressDetails = nominatimResponse.data.address;
                    var formattedAddress = `${addressDetails.road || ''}, ${addressDetails.house_number || ''}, ${addressDetails.postcode || ''} ${addressDetails.city || ''}, ${addressDetails.country || ''}`;
                    map.setView([coords[1], coords[0]], 13);
                    if (marker) {
                        map.removeLayer(marker);
                    }
                    marker = L.marker([coords[1], coords[0]]).addTo(map)
                        .bindPopup(formattedAddress)
                        .openPopup();
                }).catch(function(nominatimError) {
                    console.log(nominatimError);
                });
            } else {
                alert("Adress not found.");
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
        var nominatimAPI = `https://nominatim.openstreetmap.org/reverse?format=json&lat=${lat}&lon=${lng}&zoom=18&addressdetails=1`;

        axios.get(nominatimAPI)
            .then(function(response) {
                var addressDetails = response.data.address;
                var formattedAddress = `${addressDetails.road || ''}, ${addressDetails.house_number || ''}, ${addressDetails.postcode || ''} ${addressDetails.city || ''}, ${addressDetails.country || ''}`;
                map.setView([lat, lng], 13);
                if (marker) {
                    map.removeLayer(marker);
                }
                marker = L.marker([lat, lng]).addTo(map)
                    .bindPopup(formattedAddress)
                    .openPopup();
            })
            .catch(function(error) {
                console.log(error);
            });
    } else {
        alert("Invalid coordinates.");
    }
});