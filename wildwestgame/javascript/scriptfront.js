'use strict';

//Kartan luonti
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
const gameScreenTravel = document.querySelector('#travelmiles');
const gameScreenCurrency = document.querySelector('#currency');
const gameScreenDayCount = document.querySelector('#daycount');
const gameScreenBanditsCaptured = document.querySelector('#banditscaptured');
const gameHelpButton = document.querySelector('#pelinohjeet-button');
const dropdown = document.querySelector('#pelinohjeet-dropdown');
const gameContainer = document.querySelector('#container');
const popupImgElement = document.querySelector('#popupimg');
const popupParaElement = document.querySelector('#popuppara');
const eventPopupElement = document.querySelector('#eventpopup');
const eventPopupClose = document.querySelector('#eventclose');
gameScreen.style.display = 'none';
//eventPopupElement.style.display = 'none';

//Globaalit arvot
let playerLocation;
let playerName;
let playerLocationName;
let playerTravelMiles;
let playerBanditsCaptured;
let playerCurrency;
let playerDayCount;


async function getWeather() {
    const response = await fetch(`http://127.0.0.1:3000/findweather/${playerLocation}`);
    const data = await response.json();
    if (data.weather_code > 50) {
        console.log('Weather 1');
        gameContainer.style.backgroundImage = `url('../images/gameplaybackground1.webp')`
    }
    else if (data.weather_code > 1) {
        console.log('Weather 2');
        gameContainer.style.backgroundImage = `url('../images/gameplaybackground3.webp')`
    }
    else {
        console.log('Weather 3');
        gameContainer.style.backgroundImage = `url('../images/gameplaybackground2.webp')`
    }
}


function eventPopupOpen(image, text) {
    popupImgElement.src = image;
    popupParaElement.innerHTML = text;
    eventPopupElement.style.display = 'flex';
}


function gameScreenText() {
    gameScreenNickname.innerHTML = `Playing as: ${playerName}`;
    gameScreenLocation.innerHTML = `Current location: ${playerLocationName}`;
    gameScreenTravel.innerHTML = `Miles traveled: ${playerTravelMiles.toFixed(0)}`;
    gameScreenBanditsCaptured.innerHTML = `Bandits captured: ${playerBanditsCaptured}`;
    gameScreenCurrency.innerHTML = `Dollars: $${playerCurrency}`;
    gameScreenDayCount.innerHTML = `Days survived: ${playerDayCount}`;
}

//Markerin klikkauksesta kysytään haluaako matkustaa kyseiseen paikkaan ja päivitetään peliä sen mukaan
async function markerCLick(town) {
    let bool;
    if (playerLocation !== town[3]) {
        bool = confirm(`Do you wish to travel to ${town[2]}?`);
    }
    if (bool) {
        playerLocationName = town[2];
        map.flyTo([town[0], town[1]], 10);  //Matkustetaan paikkaan
        const response = await fetch(`http://127.0.0.1:3000/playermove/${town[3]}`); //päivitetaan sijainti backend
        const jsonData = await response.json();
        if (jsonData.arrest) {
            alert("You found a bandit!")
            //eventPopupOpen('../images/bandit2.webp', 'You found the man! After some fighting you manage to catch him')
        }
        await getStats(); //Päivitetään statsit ja sää ruudulle
        await getWeather()
    }
}

async function getLocations() {
    const response = await fetch(`http://127.0.0.1:3000/locations`);
    const locationData = await response.json();
    for (let town of locationData) {
        if (town[3] === playerLocation) { //Asetetaan kartta pelaajan paikalle
            map.setView([town[0], town[1]], 10);
        }
        L.marker([town[0], town[1]]).addTo(map).on('click', () => markerCLick(town)); //Luodaan karttaan klikattavat markkerit
    }
}

//Haetaan statsit ja päivitetään ne ruudulle
async function getStats() {
    const response = await fetch(`http://127.0.0.1:3000/getstats`);
    const jsonData = await response.json();
    console.log(jsonData);
    playerLocation = jsonData.location;
    playerBanditsCaptured = jsonData.banditsArrested
    playerTravelMiles = jsonData.travelKm * 0.62
    playerCurrency = jsonData.money
    playerDayCount = jsonData.dayCount
    gameScreenText();
}


//Pelin lataus, pelaaja syöttää usernamen, backend lataa tai luo uuden
loadUserForm.addEventListener('submit', async function(evt) {
    evt.preventDefault();
    loginScreen.style.display = 'none';
    const username = document.querySelector('#username').value;
    const response = await fetch(`http://127.0.0.1:3000/play/${username}`);
    const jsonData = await response.json(); //Haetaan pelaajan tiedot databasesta
    playerLocation = jsonData.location;
    playerName = jsonData.name;
    playerLocationName = jsonData.location
    await getWeather() //Haetaan sää pelin alustusta varten
    getLocations(); //Ladataan pelin kartta tilanne
    await getStats()
    gameScreen.style.display = 'flex';
});


/* JS SCRIPTI BUTTONEILLE */
gameHelpButton.addEventListener('click', function() {
    if (dropdown.style.display === 'none' || dropdown.style.display === '') {
        dropdown.style.display = 'block';
    } else {
        dropdown.style.display = 'none';
    }
})

//Event popup sulkemis nappi
eventPopupClose.addEventListener('click', () => eventPopupElement.style.display = 'none' );


