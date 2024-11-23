'use strict';

//Kartan luonti
const denver = [40, -105];
const map = L.map('map');
L.tileLayer('https://tile.openstreetmap.org/{z}/{x}/{y}.png', {
    maxZoom: 19,
    attribution: '&copy; <a href="http://www.openstreetmap.org/copyright">OpenStreetMap</a>',
}).addTo(map);

//HTML ELEMENTIT
const loadUserForm = document.querySelector('#usernameform');
const gameScreen = document.querySelector('#gamescreen');
const loginScreen = document.querySelector('#loginscreen');
const gameScreenNickname = document.querySelector('#nickname');
const gameScreenLocation = document.querySelector('#location');
gameScreen.style.display = 'none';

//Globaalit arvot
let playerLocation;
let playerName;

function gameScreenText() {
    gameScreenNickname.innerHTML = `Playing as: ${playerName}`;
    gameScreenLocation.innerHTML = `Current location: ${playerLocation}`;
}

//Markerin klikkauksesta kysytään haluaako matkustaa kyseiseen paikkaan ja päivitetään sijainti
function markerCLick(town) {
    const bool = confirm(`Do you wish to travel to ${town[2]}?`);
    if (bool) {
        playerLocation = town[3];
        fetch(`http://127.0.0.1:3000/playermove/${town[3]}`); //päivitetaan sijainti backend
        gameScreenText(); //Päivitetään location ruudulle
        map.flyTo([town[0], town[1]]);  //Matkustetaan paikkaan
    }
}

async function getLocations() {
    const response = await fetch(`http://127.0.0.1:3000/locations`);
    const locationData = await response.json();
    console.log(locationData);
    for (let town of locationData) {
        if (town[3] === playerLocation) { //Asetetaan kartta pelaajan paikalle
            map.setView([town[0], town[1]], 8);
        }
        L.marker([town[0], town[1]]).addTo(map).on('click', () => markerCLick(town)); //Luodaan karttaan klikattavat markkerit
    }
}

//Pelin lataus, pelaaja syöttää usernamen, backend lataa tai luo uuden
loadUserForm.addEventListener('submit', async function(evt) {
    evt.preventDefault();
    loginScreen.style.display = 'none';
    const username = document.querySelector('#username').value;
    const response = await fetch(`http://127.0.0.1:3000/load/${username}`);
    const jsonData = await response.json(); //Haetaan pelaajan tiedot databasesta
    console.log(jsonData);
    playerLocation = jsonData.location;
    playerName = jsonData.name;
    getLocations(); //Ladataan pelin kartta tilanne
    gameScreenText(); //Ladataan nimi ja location ruudulle
    gameScreen.style.display = 'block';
});


