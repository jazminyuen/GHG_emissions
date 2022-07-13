function markerSize(ghg) {
    return ghg / 20;
  }
  var data = d3.json("./static/basins.json");
  var locations2 = [];
  function getEmissions() {
    d3.json("./static/basins.json").then(d => {
      var locations2 = [];
      var features = d.features;
      // console.log(features);
      features.forEach(x => {
        var geometry = [x.geometry.coordinates[1], x.geometry.coordinates[0]];
        var city = x.properties.City;
        var state = x.properties.State;
        var totalEmissions = x.properties["Total Emissions"];
        // console.log(x);
        locations2.push({
          coordinates: geometry,
          city: city,
          totalEmissions: totalEmissions,
          state: state,
        });
      });
      var emissions2020 = [];
      var emissions2019 = [];
      var emissions2018 = [];
      var emissions2017 = [];
      var emissions2016 = [];
      var emissions2015 = [];
      var emissions2014 = [];
      var emissions2013 = [];
      var emissions2012 = [];
      var emissions2011 = [];
      var emissionstotal = [];
      var emissionsAverage = [];
      locations2.forEach(x => {
        emissions2020.push(
          L.circle(x.coordinates, {
            stroke: false,
            fillOpacity: 0.5,
            color: "black",
            fillColor: "black",
            radius: markerSize(x.totalEmissions["2020 Emissions"])
          })
        );
        emissions2019.push(
          L.circle(x.coordinates, {
            stroke: false,
            fillOpacity: 0.5,
            color: "blue",
            fillColor: "blue",
            radius: markerSize(x.totalEmissions["2019 Emissions"])
          })
        );
        emissions2018.push(
            L.circle(x.coordinates, {
              stroke: false,
              fillOpacity: 0.5,
              color: "white",
              fillColor: "white",
              radius: markerSize(x.totalEmissions["2018 Emissions"])
            })
          );
          emissions2017.push(
            L.circle(x.coordinates, {
              stroke: false,
              fillOpacity: 0.5,
              color: "orange",
              fillColor: "orange",
              radius: markerSize(x.totalEmissions["2017 Emissions"])
            })
          );
          emissions2016.push(
            L.circle(x.coordinates, {
              stroke: false,
              fillOpacity: 0.5,
              color: "purple",
              fillColor: "purple",
              radius: markerSize(x.totalEmissions["2016 Emissions"])
            })
          );
          emissions2015.push(
            L.circle(x.coordinates, {
              stroke: false,
              fillOpacity: 0.5,
              color: "green",
              fillColor: "green",
              radius: markerSize(x.totalEmissions["2015 Emissions"])
            })
          );
          emissions2014.push(
            L.circle(x.coordinates, {
              stroke: false,
              fillOpacity: 0.5,
              color: "pink",
              fillColor: "pink",
              radius: markerSize(x.totalEmissions["2014 Emissions"])
            })
          );
          emissions2013.push(
            L.circle(x.coordinates, {
              stroke: false,
              fillOpacity: 0.5,
              color: "yellow",
              fillColor: "yellow",
              radius: markerSize(x.totalEmissions["2013 Emissions"])
            })
          );
          emissions2012.push(
            L.circle(x.coordinates, {
              stroke: false,
              fillOpacity: 0.5,
              color: "purple",
              fillColor: "purple",
              radius: markerSize(x.totalEmissions["2012 Emissions"])
            })
          );
          emissions2011.push(
            L.circle(x.coordinates, {
              stroke: false,
              fillOpacity: 0.5,
              color: "red",
              fillColor: "red",
              radius: markerSize(x.totalEmissions["2011 Emissions"])
            })
          );
          emissionstotal.push(
            L.circle(x.coordinates, {
              stroke: false,
              fillOpacity: 0.5,
              color: "red",
              fillColor: "red",
              radius: (x.totalEmissions["Total Emissions"])/80
            })
            
          );
          emissionsAverage.push(
            L.circle(x.coordinates, {
              stroke: false,
              fillOpacity: 0.5,
              color: "red",
              fillColor: getColor(x.totalEmissions["Average Emissions"]),
              radius: x.totalEmissions["Average Emissions"]/8
            })
            
          );

          function getColor(x) {
            if (x > 285271.891) {
            return "red";
            }
            if (x >= 102890.58 &  x <= 285271.891) {
            return "blue";
            }
        
            if (x < 102890.58) {
            return "green";
            }
        }
          
          
      })
      console.log(locations2);
      // Streetmap Layer
      var streetmap = L.tileLayer("https://api.mapbox.com/styles/v1/{id}/tiles/{z}/{x}/{y}?access_token={accessToken}", {
        attribution: "© <a href='https://www.mapbox.com/about/maps/'>Mapbox</a> © <a href='http://www.openstreetmap.org/copyright'>OpenStreetMap</a> <strong><a href='https://www.mapbox.com/map-feedback/' target='_blank'>Improve this map</a></strong>",
        tileSize: 512,
        maxZoom: 18,
        zoomOffset: -1,
        id: "mapbox/streets-v11",
        accessToken: API_KEY
      });
  
      var darkmap = L.tileLayer("https://api.mapbox.com/styles/v1/mapbox/{id}/tiles/{z}/{x}/{y}?access_token={accessToken}", {
        attribution: "Map data &copy; <a href=\"https://www.openstreetmap.org/\">OpenStreetMap</a> contributors, <a href=\"https://creativecommons.org/licenses/by-sa/2.0/\">CC-BY-SA</a>, Imagery © <a href=\"https://www.mapbox.com/\">Mapbox</a>",
        maxZoom: 18,
        id: "dark-v10",
        accessToken: API_KEY
      });
  
      var night = L.tileLayer("https://api.mapbox.com/styles/v1/mapbox/{id}/tiles/{z}/{x}/{y}?access_token={accessToken}", {
        attribution: "Map data &copy; <a href=\"https://www.openstreetmap.org/\">OpenStreetMap</a> contributors, <a href=\"https://creativecommons.org/licenses/by-sa/2.0/\">CC-BY-SA</a>, Imagery © <a href=\"https://www.mapbox.com/\">Mapbox</a>",
        maxZoom: 18,
        id: "navigation-night-v1",
        accessToken: API_KEY
      });
      var outdoors = L.tileLayer("https://api.mapbox.com/styles/v1/mapbox/{id}/tiles/{z}/{x}/{y}?access_token={accessToken}", {
        attribution: "Map data &copy; <a href=\"https://www.openstreetmap.org/\">OpenStreetMap</a> contributors, <a href=\"https://creativecommons.org/licenses/by-sa/2.0/\">CC-BY-SA</a>, Imagery © <a href=\"https://www.mapbox.com/\">Mapbox</a>",
        maxZoom: 18,
        id: "outdoors-v11",
        accessToken: API_KEY
      });
  
      // Create two separate layer groups below. One for city markers, and one for states markers
      var baseMaps = {
        "Street Map": streetmap,
        "Dark Map": darkmap,
        "Night Map": night,
        "Outdoors Map": outdoors,
      }
      // Create a baseMaps object to contain the streetmap and darkmap
      // var cityMarkers = [];
      // var stateMarkers = [];
  
      // Create an overlayMaps object here to contain the "State Population" and "City Population" layers
      var em_2020 = L.layerGroup(emissions2020);
      var em_2019 = L.layerGroup(emissions2019);
      var em_2018 = L.layerGroup(emissions2018);
      var em_2017 = L.layerGroup(emissions2017);
      var em_2016 = L.layerGroup(emissions2016);
      var em_2015 = L.layerGroup(emissions2015);
      var em_2014 = L.layerGroup(emissions2014);
      var em_2013 = L.layerGroup(emissions2013);
      var em_2012 = L.layerGroup(emissions2012);
      var em_2011 = L.layerGroup(emissions2011);
      var em_total = L.layerGroup(emissionstotal);
      var em_avg = L.layerGroup(emissionsAverage);
      var overlayMaps = {
        "2020 Emissions": em_2020,
        "2019 Emissions": em_2019,
        "2018 Emissions": em_2018,
        "2017 Emissions": em_2017,
        "2016 Emissions": em_2016,
        "2015 Emissions": em_2015,
        "2014 Emissions": em_2014,
        "2013 Emissions": em_2013,
        "2012 Emissions": em_2012,
        "2011 Emissions": em_2011,
        "Total Emissions (2011-2019)": em_total,
        "Average Emissions (2011-2019)": em_avg
      }
  
      // Modify the map so that it will have the streetmap, states, and cities layers
      var myMap = L.map("mapid", {
        center: [
          37.09, -95.71
        ],
        zoom: 5,
        layers: [streetmap]
      });
  
      // Create a layer control, containing our baseMaps and overlayMaps, and add them to the map
      L.control.layers(baseMaps, overlayMaps, {
        collapsed: false
      }).addTo(myMap);
    })
  
  }
  locations2 = getEmissions();
  console.log(locations2);