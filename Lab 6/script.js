// Initialize map
var map = L.map('map').setView([51.0447, -114.0719], 12);

// Add OpenStreetMap basemap
L.tileLayer('https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png', {
    attribution: 'OpenStreetMap'
}).addTo(map);


// Feature group to store drawn items
var drawnItems = new L.FeatureGroup();
map.addLayer(drawnItems);


// Draw control (only allow polyline)
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


// Variable to store the drawn polyline
var drawnLine = null;


// When a polyline is created
map.on(L.Draw.Event.CREATED, function (event) {

    var layer = event.layer;

    // store the line
    drawnLine = layer;

    // add to map
    drawnItems.addLayer(layer);

});