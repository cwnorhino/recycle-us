let map;
let userMarker;

function initMap() {
    map = L.map('map').setView([0, 0], 12);

    L.tileLayer('https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png', {
        attribution: '© OpenStreetMap contributors'
    }).addTo(map);

    if ("geolocation" in navigator) {
        navigator.geolocation.getCurrentPosition(
            (position) => {
                const userLocation = {
                    lat: position.coords.latitude,
                    lng: position.coords.longitude
                };

                map.setView([userLocation.lat, userLocation.lng], 12);

                userMarker = L.marker([userLocation.lat, userLocation.lng], {
                    icon: L.icon({
                        iconUrl: 'https://raw.githubusercontent.com/pointhi/leaflet-color-markers/master/img/marker-icon-2x-blue.png',
                        shadowUrl: 'https://cdnjs.cloudflare.com/ajax/libs/leaflet/0.7.7/images/marker-shadow.png',
                        iconSize: [25, 41],
                        iconAnchor: [12, 41],
                        popupAnchor: [1, -34],
                        shadowSize: [41, 41]
                    })
                }).addTo(map)
                    .bindPopup('Your Location')
                    .openPopup();

                fetchAndAddRecyclingCenters(userLocation.lat, userLocation.lng);
            },
            () => {
                handleLocationError(true);
            }
        );
    } else {
        handleLocationError(false);
    }
}

function handleLocationError(browserHasGeolocation) {
    alert(browserHasGeolocation ?
        'Error: The Geolocation service failed.' :
        'Error: Your browser doesn\'t support geolocation.');
}

let recyclingMarkers = [];

function fetchAndAddRecyclingCenters(lat, lng) {
    // Clear existing markers
    recyclingMarkers.forEach(marker => marker.remove());
    recyclingMarkers = [];

    fetch(`/get_recycling_centers?lat=${lat}&lng=${lng}`)
        .then(response => response.json())
        .then(centers => {
            centers.forEach(center => {
                const marker = L.marker([center.latitude, center.longitude])
                    .addTo(map)
                    .bindPopup(center.name);
                recyclingMarkers.push(marker);
            });
        })
        .catch(error => console.error('Error fetching recycling centers:', error));
}

document.addEventListener('DOMContentLoaded', initMap);