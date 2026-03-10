var osm = L.tileLayer('https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png', {
    attribution: 'OpenStreetMap'
});

var mapboxLayer = L.tileLayer(
'https://api.mapbox.com/styles/v1/{id}/tiles/{z}/{x}/{y}?access_token=' + MAPBOX_TOKEN,
{
    attribution: '© Mapbox © OpenStreetMap',
    tileSize: 512,
    zoomOffset: -1,
    id: 'chethankarthikeya/cmmkvtxfo008y01spezav6fs5'
});

var map = L.map('map', {
    center: [51.0447, -114.0719],
    zoom: 11,
    layers: [osm]
});

var baseMaps = {
    "OpenStreetMap": osm
};

var overlayMaps = {
    "Traffic Incidents 2017": mapboxLayer
};

L.control.layers(baseMaps, overlayMaps).addTo(map);
var markers = L.markerClusterGroup();
map.addLayer(markers);
var oms = new OverlappingMarkerSpiderfier(map);

function searchPermits() {

    var start = document.getElementById("start").value;
    var end = document.getElementById("end").value;

    var message = document.getElementById("message");
    var spinner = document.getElementById("spinner");

    message.innerHTML = "";

    // Validate dates
    if (!start || !end) {
        message.innerHTML = "Please select both start and end dates.";
        return;
    }

    if (start > end) {
        message.innerHTML = "Start date cannot be after end date.";
        return;
    }

    markers.clearLayers();

    spinner.style.display = "block";

    fetch(`/search?start=${start}&end=${end}`)
        .then(response => response.json())
        .then(data => {

            spinner.style.display = "none";

            markers.clearLayers();

            if (!data.features || data.features.length === 0) {
                message.innerHTML = "No building permits found for this date range.";
                return;
            }

            var geojsonLayer = L.geoJSON(data, {

                onEachFeature: function (feature, layer) {

                    var p = feature.properties;

                    layer.bindPopup(
                        "Issued Date: " + p.issueddate +
                        "<br>Work Class: " + p.workclassgroup +
                        "<br>Contractor: " + p.contractorname +
                        "<br>Community: " + p.communityname +
                        "<br>Address: " + p.originaladdress
                    );

                    oms.addMarker(layer);
                }

            }).addTo(markers);

            map.fitBounds(geojsonLayer.getBounds());

        })
        .catch(error => {

            spinner.style.display = "none";

            message.innerHTML = "Error retrieving data. Please try again.";

            console.error(error);
        });
}