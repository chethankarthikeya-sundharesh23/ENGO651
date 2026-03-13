// Initialize map
var map = L.map('map').setView([51.0447, -114.0719], 12);

// Add OpenStreetMap basemap
L.tileLayer('https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png', {
    attribution: 'OpenStreetMap'
}).addTo(map);

// Feature group for drawn items
var drawnItems = new L.FeatureGroup();
map.addLayer(drawnItems);


// Draw control
var drawControl = new L.Control.Draw({
    draw: {
        polyline: true,
        polygon: false,
        rectangle: false,
        circle: false,
        marker: false,
        circlemarker: false
    },
    edit: {
        featureGroup: drawnItems
    }
});

map.addControl(drawControl);


// Variables
var drawnLine = null;
var simplifiedLine = null;


// When user draws a line
map.on(L.Draw.Event.CREATED, function (event) {

    var layer = event.layer;

    drawnLine = layer;

    drawnItems.addLayer(layer);

});


// Simplify button
document.getElementById("simplifyBtn").onclick = function () {

    if (!drawnLine) {
        alert("Draw a polyline first!");
        return;
    }

    // Convert to GeoJSON
    var geojson = drawnLine.toGeoJSON();

    // Simplify using Turf.js
    var simplified = turf.simplify(geojson, {
        tolerance: 0.01,
        highQuality: true
    });

    // Remove old simplified line if it exists
    if (simplifiedLine) {
        map.removeLayer(simplifiedLine);
    }

    // Add simplified line to map
    simplifiedLine = L.geoJSON(simplified, {
        style: {
            color: "red",
            weight: 4
        }
    }).addTo(map);

};