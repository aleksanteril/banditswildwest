//Backend yhteys on 127.0.0.1:3000 kautta
//Endpointit määritetään tähän
'use strict';

async function getLocations()  {
  const response = await fetch(`http://127.0.0.1:3000/locations`);
  const locationData = await response.json();
  console.log(locationData)
  for (let town of locationData) {
    console.log(town)
    L.marker([town[0], town[1]]).addTo(map);
  }
}



const loadUserForm = document.querySelector('#usernameform')
loadUserForm.addEventListener('submit', async function(evt) {
        evt.preventDefault();
        const username = document.querySelector('#username').value;
        const response = await fetch(`http://127.0.0.1:3000/load/${username}`);
        const jsonData = await response.json();
        console.log(jsonData)
});

const denver = [39.742043, -104.991531];
const map = L.map('map').setView(denver, 8);
L.tileLayer('https://tile.openstreetmap.org/{z}/{x}/{y}.png', {
    maxZoom: 19,
    attribution: '&copy; <a href="http://www.openstreetmap.org/copyright">OpenStreetMap</a>'
}).addTo(map);

//Lisätään pisteet kartalle funktio
var locationMarkers = new L.FeatureGroup().addTo(map);
getLocations();