// Initialize the map
var map = L.map('map').setView([0, 0], 2);

// Add the OpenStreetMap tile layer
L.tileLayer('https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png', {
    attribution: '© OpenStreetMap contributors'
}).addTo(map);

// Fetch recycling centers from the server
fetch('/get_recycling_centers')
    .then(response => response.json())
    .then(centers => {
        centers.forEach(center => {
            addMarker(center.latitude, center.longitude, center.name);
        });
    });

// Function to add a marker
function addMarker(lat, lon, name) {
    L.marker([lat, lon]).addTo(map)
        .bindPopup(name);
}

// Center the map on the user's location if available
if ("geolocation" in navigator) {
    navigator.geolocation.getCurrentPosition(function (position) {
        var lat = position.coords.latitude;
        var lon = position.coords.longitude;
        map.setView([lat, lon], 10);
        addMarker(lat, lon, "Your Location");
    });
}