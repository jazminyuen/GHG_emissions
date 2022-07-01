// Add console.log to check to see if our code is working.
console.log("working");

// Create the map object with a center and zoom level.
let map = L.map("mapid", {
  center: [
    40.7, -94.5
  ],
  zoom: 4
});

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
streets.addTo(map);


// Accessing the basin GeoJSON data
let basinData = "https://raw.githubusercontent.com/jazminyuen/GHG_emissions/vanessa/basins_map/static/basins.json";



// Grabbing our GeoJSON data.
d3.json(basinData).then(function (x) {
  console.log(x);
  // Creating a GeoJSON layer with the retrieved data.
  L.geoJSON(x).addTo(map);
  
});


// d3.json(basinData).then(function(data) {
//   for (var i = 0; i < data.length; i++) {
//     console.log(data[i].geometry.coordinates);
//     L.marker(data[i].geometry.coordinates).addTo(map);
//       //console.log(data[i].properties);
//   }
// });