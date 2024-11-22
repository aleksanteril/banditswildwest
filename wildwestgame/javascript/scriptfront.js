'use strict';

//Täällä funktiossa tehdään kaikki markerin klikkaukseen liittyvät jutut!!!!
function markerCLick() {
  confirm("Do you wish to travel to: {");
}

async function getLocations() {
  const response = await fetch(`http://127.0.0.1:3000/locations`);
  const locationData = await response.json();
  console.log(locationData);
  for (let town of locationData) {
    console.log(town);
    L.marker([town[0], town[1]]).addTo(map).on('click', () => {
      const bool = confirm(`Do you wish to travel to ${town[2]}?`)
      if (bool) {
        playerLocation = town[3]
        fetch(`http://127.0.0.1:3000/updatelocation/${town[3]}`) //päivitetaan sijainti backend
        console.log(playerLocation)
        //TÄHÄN UPDATE PLAYER LOCATION BACKEND -> DATABASE JA LOGIIKKA LASKEE MITÄ TAPAHTUU
      };
    });
  }
}


//Pelin lataus, pelaaja syöttää usernamen, backend lataa tai luo uuden
const loadUserForm = document.querySelector('#usernameform');
loadUserForm.addEventListener('submit', async function(evt) {
  evt.preventDefault();
  const username = document.querySelector('#username').value;
  const response = await fetch(`http://127.0.0.1:3000/load/${username}`);
  const jsonData = await response.json();
  console.log(jsonData); //Haetaan pelaajan tiedot databasesta
  playerLocation = jsonData.location;
  console.log(playerLocation);
  getLocations();
});

//Kartan luonti
const denver = [40, -105];
const map = L.map('map').setView(denver, 8);
L.tileLayer('https://tile.openstreetmap.org/{z}/{x}/{y}.png', {
  maxZoom: 19,
  attribution: '&copy; <a href="http://www.openstreetmap.org/copyright">OpenStreetMap</a>',
}).addTo(map);

//Globaalit arvot
let playerLocation;

//HISTORIALLISEN KARTAN LUONTI YRITYS, EI TOIMI, TARVITSEE VIELÄ MAPLIBREGL DATES TOIMIAKSEEN
//const gl = L.maplibreGL({
//  style: 'https://www.openhistoricalmap.org/map-styles/main/main.json',
//  attributionControl: '<a href="https://www.openhistoricalmap.org/">OpenHistoricalMap</a>'
//}).addTo(map);
//
//const maplibreMap = gl.getMaplibreMap();
//maplibreMap.once('styledata', function (event) {
//    maplibreMap.filterByDate(map, '1939-08-31');
//});

//Lisätään pisteet kartalle funktio ja aluestetaan kartta
//var locationMarkers = new L.FeatureGroup().addTo(map);

