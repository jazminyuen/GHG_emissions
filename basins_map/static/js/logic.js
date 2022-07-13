// Add console.log to check to see if our code is working.
console.log("working");

// Create the map object with a center and zoom level.


// We create the tile layer that will be the background of our map.
let streets = L.tileLayer('https://api.mapbox.com/styles/v1/{id}/tiles/{z}/{x}/{y}?access_token={accessToken}', {
  attribution: 'Map data &copy; <a href="https://www.openstreetmap.org/">OpenStreetMap</a> contributors, <a href="https://creativecommons.org/licenses/by-sa/2.0/">CC-BY-SA</a>, Imagery © <a href="https://www.mapbox.com/">Mapbox</a>',
  maxZoom: 18,
  id: 'mapbox/streets-v11',
  tileSize: 512,
  zoomOffset: -1,
  accessToken: API_KEY
});
// Add our 'graymap' tile layer to the map.
// streets.addTo(map);

let map = L.map("mapid", {
  center: [
    40.7, -94.5
  ],
  zoom: 4,
  layers: [streets]
});



// Define an object that contains the overlays.
// This overlay will be visible all the time.

// let layergroups = [emissions_2011, emissions_2012, emissions_2013]
// Accessing the basin GeoJSON data
// let basinData = "https://raw.githubusercontent.com/jazminyuen/GHG_emissions/vanessa/basins_map/static/basins.json";
let basinData = "./static/basins.json";



// Grabbing our GeoJSON data.
// d3.json(basinData).then(function (x) {
//console.log(x);
// Creating a GeoJSON layer with the retrieved data.
//L.geoJSON(x).addTo(map);

// });

var layergroups = {
  "2011": [],
  "2012": [],
  "2013": [],
}
var c2011 = [];

d3.json(basinData).then(function (data) {
  //console.log(data);
  // Creating a GeoJSON layer with the retrieved data.
  console.log(data.features);
  data.features.forEach(element => {
    // console.log(element.properties["Total Emissions"]);
    coordinates = [element.geometry.coordinates[1], element.geometry.coordinates[0]];
    var v2011 = L.circle(coordinates);
    // v2011.addTo(map)
    console.log(v2011);
    c2011.push(v2011);
    layergroups["2012"].push(L.circle(coordinates, {
      title: element.properties["Total Emissions"]["2012 Emissions"],
      radius:5000
    }).bindPopup(`${element.properties["City"]}, ${element.properties["State"]}`));
    layergroups["2013"].push(L.circle(coordinates, {
      title: element.properties["Total Emissions"]["2013 Emissions"],
      radius:5000
    }).bindPopup(`${element.properties["City"]}, ${element.properties["State"]}`));
    
    
  });
  // L.geoJSON(data, {

  // // We turn each feature into a circleMarker on the map.

  //   pointToLayer: function(feature, latlng) {
  //               console.log(feature);
  //               return L.circleMarker(latlng);
  //           },
  //       }).addTo(map);
});


// d3.json(basinData).then(function(data) {
//   for (var i = 0; i < data.length; i++) {
//     console.log(data[i].geometry.coordinates);
//     L.marker(data[i].geometry.coordinates).addTo(map);
//       //console.log(data[i].properties);
//   }
// });
console.log(c2011);
// Create the earthquake, tectonic plate, and major earthquake layer for our map.
let emissions_2011 = L.layerGroup(c2011);
let emissions_2012 = L.layerGroup(layergroups["2012"]);
let emissions_2013 = L.layerGroup(layergroups["2013"]);
let emissions_2014 = L.layerGroup();
let emissions_2015 = L.layerGroup();
let emissions_2016 = L.layerGroup();
let emissions_2017 = L.layerGroup();
let emissions_2018 = L.layerGroup();
let emissions_2019 = L.layerGroup();
emissions_2011.addTo(map)
let overlays = {
  "2011 Emissions": emissions_2011,
  "2012 Emissions": emissions_2012,
  "2013 Emissions": emissions_2013,
  "2014 Emissions": emissions_2014,
  "2015 Emissions": emissions_2015,
  "2016 Emissions": emissions_2016,
  "2017 Emissions": emissions_2017,
  "2018 Emissions": emissions_2018,
  "2019 Emissions": emissions_2019,
};

let baseMap = {
  "Street": streets,
};

console.log(c2011.length);
layergroups["2011"].forEach(x=>{
  console.log(x);
  x.addTo(map)});
// Then we add a control to the map that will allow the user to change
// which layers are visible.
L.control.layers(baseMap, overlays).addTo(map);

