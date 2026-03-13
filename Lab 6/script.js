// Initialize map
var map = L.map('map').setView([51.0447, -114.0719], 12);

// Basemap
L.tileLayer('https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png', {
    attribution:'OpenStreetMap'
}).addTo(map);


// Feature group
var drawnItems = new L.FeatureGroup();
map.addLayer(drawnItems);


// Draw controls
var drawControl = new L.Control.Draw({
    draw:{
        polyline:true,
        polygon:false,
        rectangle:false,
        circle:false,
        marker:false,
        circlemarker:false
    },
    edit:{
        featureGroup:drawnItems
    }
});

map.addControl(drawControl);


// Variables
var drawnLine=null;
var simplifiedLine=null;


// When user draws
map.on(L.Draw.Event.CREATED,function(event){

    var layer=event.layer;

    drawnLine=layer;

    drawnItems.addLayer(layer);

});


// ------------------
// Custom Control UI
// ------------------

var control = L.control({position:'topleft'});

control.onAdd=function(map){

var div=L.DomUtil.create('div','custom-control');

div.innerHTML=
'<button id="simplifyBtn">Simplify</button>'+
'<button id="clearBtn">Clear</button>'+
'<div class="stats">Original: <span id="originalPts">0</span></div>'+
'<div class="stats">Simplified: <span id="simplifiedPts">0</span></div>';

return div;

};

control.addTo(map);


// Prevent map dragging when clicking buttons
document.addEventListener("DOMContentLoaded", function(){
var controlDiv=document.querySelector('.custom-control');
L.DomEvent.disableClickPropagation(controlDiv);
});


// Simplify function
function simplifyLine(){

if(!drawnLine){
alert("Draw a polyline first!");
return;
}

var geojson=drawnLine.toGeoJSON();

var originalPoints=geojson.geometry.coordinates.length;

var simplified=turf.simplify(geojson,{
tolerance:0.01,
highQuality:true
});

var simplifiedPoints=simplified.geometry.coordinates.length;

document.getElementById("originalPts").textContent=originalPoints;
document.getElementById("simplifiedPts").textContent=simplifiedPoints;


if(simplifiedLine){
map.removeLayer(simplifiedLine);
}

simplifiedLine=L.geoJSON(simplified,{
style:{
color:"red",
weight:4
}
}).addTo(map);

}


// Clear function
function clearMap(){

if(drawnLine){
drawnItems.removeLayer(drawnLine);
drawnLine=null;
}

if(simplifiedLine){
map.removeLayer(simplifiedLine);
simplifiedLine=null;
}

document.getElementById("originalPts").textContent=0;
document.getElementById("simplifiedPts").textContent=0;

}


// Wait for buttons to exist
setTimeout(function(){

document.getElementById("simplifyBtn").onclick=simplifyLine;
document.getElementById("clearBtn").onclick=clearMap;

},100);