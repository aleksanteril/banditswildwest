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
let playerLocationName;
let banditLocation;



function gameScreenText() {
    gameScreenNickname.innerHTML = `Playing as: ${playerName}`;
    gameScreenLocation.innerHTML = `Current location: ${playerLocationName}`;
}

//Markerin klikkauksesta kysytään haluaako matkustaa kyseiseen paikkaan ja päivitetään sijainti
async function markerCLick(town) {
    let bool;
    if (playerLocation !== town[3]) {
        bool = confirm(`Do you wish to travel to ${town[2]}?`);
    }
    if (bool) {
        playerLocation = town[3];
        playerLocationName = town[2];
        const response = await fetch(`http://127.0.0.1:3000/playermove/${town[3]}`); //päivitetaan sijainti backend
        const jsonData = await response.json();
        console.log(jsonData);
        map.flyTo([town[0], town[1]], 10);  //Matkustetaan paikkaan
        if (jsonData.arrest) {
            alert("You found a bandit!")
            banditLocation = jsonData.banditLocation;
        }
        gameScreenText(); //Päivitetään location ruudulle
        getStats();
    }
}

async function getLocations() {
    const response = await fetch(`http://127.0.0.1:3000/locations`);
    const locationData = await response.json();
    console.log(locationData);
    for (let town of locationData) {
        if (town[3] === playerLocation) { //Asetetaan kartta pelaajan paikalle
            map.setView([town[0], town[1]], 10);
            playerLocationName = town[2];
        }
        L.marker([town[0], town[1]]).addTo(map).on('click', () => markerCLick(town)); //Luodaan karttaan klikattavat markkerit
    }
    gameScreenText();
    getStats();
}

async function getStats() {
    const response = await fetch(`http://127.0.0.1:3000/getstats`);
    const jsonData = await response.json();
    console.log(jsonData);
}


//Pelin lataus, pelaaja syöttää usernamen, backend lataa tai luo uuden
loadUserForm.addEventListener('submit', async function(evt) {
    evt.preventDefault();
    loginScreen.style.display = 'none';
    const username = document.querySelector('#username').value;
    const response = await fetch(`http://127.0.0.1:3000/play/${username}`);
    const jsonData = await response.json(); //Haetaan pelaajan tiedot databasesta
    console.log(jsonData);
    playerLocation = jsonData.location;
    playerName = jsonData.name;
    banditLocation = jsonData.banditLocation;
    getLocations(); //Ladataan pelin kartta tilanne
    gameScreen.style.display = 'block';
});


/* JS SCRIPTI BUTTONEILLE */
document.querySelector('#pelinohjeet-button').addEventListener('click', function() {
    let dropdown = document.querySelector('#pelinohjeet-dropdown');
    if (dropdown.style.display === 'none' || dropdown.style.display === '') {
        dropdown.style.display = 'block';
    } else {
        dropdown.style.display = 'none';
    }
})

