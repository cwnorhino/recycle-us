// Initialize the map
var map = L.map('map').setView([0, 0], 2);

// Add the OpenStreetMap tile layer
L.tileLayer('https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png', {
    attribution: '© OpenStreetMap contributors'
}).addTo(map);

// Function to add a marker
function addMarker(lat, lon, name) {
    L.marker([lat, lon]).addTo(map)
        .bindPopup(name);
}

// Replace these with actual data from your database in the future
addMarker(26.9432, 75.7755, "Ecto E Waste Recycler Pvt Ltd");
addMarker(26.2637, 73.0130, "Laxmi Plastics");

// Center the map on the user's location if available
if ("geolocation" in navigator) {
    navigator.geolocation.getCurrentPosition(function (position) {
        var lat = position.coords.latitude;
        var lon = position.coords.longitude;
        map.setView([lat, lon], 10);
        addMarker(lat, lon, "Your Location");
    });
}