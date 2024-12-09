'use strict';

//Kartan luonti
const map = L.map('map');
L.tileLayer('https://tile.openstreetmap.org/{z}/{x}/{y}.png', {
    maxZoom: 7.5,
    attribution: '&copy; <a href="http://www.openstreetmap.org/copyright">OpenStreetMap</a>',
}).addTo(map);

//Vihreä ikoni
const greenIcon = new L.Icon({
  iconUrl: 'https://raw.githubusercontent.com/pointhi/leaflet-color-markers/master/img/marker-icon-2x-green.png',
  shadowUrl: 'https://cdnjs.cloudflare.com/ajax/libs/leaflet/0.7.7/images/marker-shadow.png',
  iconSize: [25, 41],
  iconAnchor: [12, 41],
  popupAnchor: [1, -34],
  shadowSize: [41, 41]
});



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
const eventPopupCloseButton = document.querySelector('#eventclose');
const terminalHTML = document.querySelector('#terminal');
const gameLeaderboardButton = document.querySelector('#leaderboard-button');
const gameLeaderboardDropdown = document.querySelector('#leaderboard-dropdown');
const leaderboardContent = document.querySelector('#leaderboard-content');
const leaderboardHeaders = document.querySelector('#leaderboard-headers');

//Globaalit arvot
let playerLocation;
let playerName;
let playerLocationName;
let playerTravelMiles;
let playerBanditsCaptured;
let playerCurrency;
let playerDeathCount;
let soundtrack;
let eventSound;
let towns;

//funktio leaderboardille
async function leaderboardDropdown() {
    const response = await fetch(`http://127.0.0.1:3000/leaderboard`);
    const data = await response.json(); // [name0, bandits1, money2, totalKM3, deathcount4]
    const headerNamesList = ['Name', 'Money', 'Bandits', 'Deaths'];
    const headerRow = document.createElement('tr');

    for (let headerName of headerNamesList) {
        const header = document.createElement('th');
        const headerText = document.createTextNode(headerName);
        header.appendChild(headerText);
        headerRow.appendChild(header);
    }
    leaderboardHeaders.appendChild(headerRow);

    for (let row of data) {
        const tableRow = document.createElement('tr');

        const name = document.createElement('td');
        const nameText = document.createTextNode(row[0]);
        name.appendChild(nameText);
        tableRow.appendChild(name);

        const money = document.createElement('td');
        const moneyText = document.createTextNode(`$${row[2]}`);
        money.appendChild(moneyText);
        tableRow.appendChild(money);

        const bandits = document.createElement('td');
        const banditsText = document.createTextNode(row[1]);
        bandits.appendChild(banditsText);
        tableRow.appendChild(bandits);

        const deaths = document.createElement('td');
        const deathsText = document.createTextNode(`☠ ${row[4]}`); // Placeholderi kuolemille
        deaths.appendChild(deathsText);
        tableRow.appendChild(deaths);

        leaderboardContent.appendChild(tableRow);
    }
}

// funktio eventsoundeille
function playEventSound(popSound) {
    eventSound = new Audio(popSound);
    eventSound.autoplay = true;
}

//Sään haku background kuvaa varten
async function getWeather(background) {
    const response = await fetch(
        `http://127.0.0.1:3000/findweather/${playerLocation}`);
    const data = await response.json();
    if (data.weather_code > 50) {
        console.log('Weather 1 rainy');
        gameContainer.style.backgroundImage = `${background}, url('../images/rainy.webp')`;
        gameContainer.style.backgroundColor = "rgba(0, 128, 255, 0.5)";
    } else if (data.weather_code > 1) {
        console.log('Weather 2 cloudy');
        gameContainer.style.backgroundImage = `${background}, url('../images/clouds3.webp')`;
        gameContainer.style.backgroundColor = "rgba(112, 128, 144, 0.5)";
    } else {
        console.log('Weather 3 sunny');
        gameContainer.style.backgroundImage = `${background}, url('../images/sunray.webp')`;
        gameContainer.style.backgroundColor = "rgba(255, 165, 0, 0.25)";
    }
}

//Rainy Weather
//A soft gray: rgb(169, 169, 169)
//A deep blue: rgb(0, 0, 139)
//A gentle teal: rgb(0, 128, 128)

//Cloudy Weather
//A light gray: rgb(211, 211, 211)
//A muted blue: rgb(112, 128, 144)
//A soft white: rgb(240, 248, 255)

//Sunny Weather
//A bright yellow: rgb(255, 223, 0)
//A warm orange: rgb(255, 165, 0)
//A clear sky blue: rgb(135, 206, 235)

//Vaihtaa backgroundin - lokaatio riippuvainen
async function getBackground(location) {
    switch(location) {
        case "Centennial":
            return `url('../images/centennial.webp')`;
        case "Buckley":
            return `url('../images/buckley.webp')`;
        case "Rocky Mountain":
            return `url('../images/rockymountain.webp')`;
        case "Provo-Utah Lake":
            return `url('../images/provoutahlake.webp')`;
        case "San Luis Valley":
            return `url('../images/sanluisvalley.webp')`;
        case "City of Colorado Springs":
            return `url('../images/coloradosprings.webp')`;
        case "Saint George-Southwest Utah":
            return `url('../images/saintgeorge.webp')`;
        case "Cedar City":
            return `url('../images/cedarcity.webp')`;
        case "Bryce Canyon":
            return `url('../images/brycecanyon.webp')`;
        case "Wendover":
            return `url('../images/wendover.webp')`;
        case "South Valley":
            return `url('../images/southvalley.webp')`;
        case "Hill":
            return `url('../images/hill.webp')`;
        case "Ogden Hinckley":
            return `url('../images/ogdenhinckley.webp')`;
        case "Logan-Cache":
            return `url('../images/logancache.webp')`;
        case "Vernal":
            return `url('../images/vernal.webp')`;
        case "Grand Junction":
            return `url('../images/grandjunction.webp')`;
        case "Montrose":
            return `url('../images/montrose.webp')`;
        case "Garfield County":
            return `url('../images/garfieldcounty.webp')`;
        case "Aspen-Pitkin Co/Sardy Field":
            return `url('../images/aspenpitkin.webp')`;
        case "Eagle County":
            return `url('../images/eaglecounty.webp')`;
        case "Butts AAF (Fort Carson)":
            return `url('../images/fortcarson.webp')`;
        case "Pueblo":
            return `url('../images/pueblo.webp')`;
    }
}

function terminalText(text) {
    const p = document.createElement('p');
    p.innerText = text;
    terminalHTML.appendChild(p)
    if (terminalHTML.childElementCount < 4) return;
    terminalHTML.removeChild(terminalHTML.firstChild);
}

//Popup funktio
function eventPopupOpen(image, text) {
    popupImgElement.src = image;
    popupParaElement.innerHTML = text;
    eventPopupElement.style.display = 'flex';
}

function eventPopupClose() {
    eventPopupElement.style.display = 'none';
    popupImgElement.src = '';
    popupParaElement.innerHTML = '';
}

function deathScreen() {
    gameScreen.style.display = 'none';
    gameContainer.style.background = 'none';
    gameContainer.style.backgroundImage = 'none';
    gameContainer.style.backgroundColor = 'black';
    const p = document.createElement('p');
    const text = document.createTextNode('You Died');
    p.appendChild(text);
    p.style.color = 'red';
    p.style.fontSize = '10rem';
    p.style.height = '45%';
    p.classList.add('deathtext');
    eventPopupCloseButton.addEventListener('click',() => gameContainer.appendChild(p));
}

//Ruudulle statsien päivitys
function gameScreenText() {
    gameScreenNickname.innerHTML = `Playing as: ${playerName}`;
    gameScreenLocation.innerHTML = `Current location: ${playerLocationName}`;
    gameScreenTravel.innerHTML = `Miles traveled: ${playerTravelMiles.toFixed(
        0)}`;
    gameScreenBanditsCaptured.innerHTML = `Bandits captured: ${playerBanditsCaptured}`;
    gameScreenCurrency.innerHTML = `Dollars: $${playerCurrency}`;
    gameScreenDayCount.innerHTML = `Deaths: ${playerDeathCount}`;
}

async function eventRequest(username){
    const response = await fetch (`http://127.0.0.1:3000/events/${username}`);
    const event = await response.json();
    eventPopupOpen(event.image, event.text);
    playEventSound(event.audio);
    terminalText(event.terminaltext);
    if (event.banditFound) await getLocations(false);
    return event.terminaltext === 'Death'; //Death bit, true jos kuoli
}

//Markerin klikkauksesta kysytään haluaako matkustaa kyseiseen paikkaan ja päivitetään peliä sen mukaan
async function markerCLick(town, marker) {
    let bool;
    if (playerLocation !== town[3]) {
        bool = confirm(`Do you wish to travel to ${town[2]}?`);
    }
    if (!bool) return; //Jos pelaaja palauttaa false confirm, palataan pois
    marker.setIcon(greenIcon)
    terminalText(`You have traveled to ${town[2]}`)
    playerLocationName = town[2];
    playerLocation = town[3]
    await map.flyTo([town[0], town[1]], 6.5);  //Matkustetaan paikkaan
    await fetch(`http://127.0.0.1:3000/playermove/${town[3]}/${playerName}`); //päivitetaan sijainti backend
    if (await eventRequest(playerName)) { //Kuolema true
        deathScreen()
        return;
    }
    await getStats(playerName); //Päivitetään statsit ja sää ruudulle
    const background = await getBackground(town[2])
    await getWeather(background);
}

//Pelin paikkojen haku ja kartta markkerien luonti
async function getLocations(first=true) {
    if (first) {
        const response = await fetch(`http://127.0.0.1:3000/locations`);
        towns = await response.json()
    }
    for (let town of towns) {
        let marker = L.marker([town[0], town[1]]).
            addTo(map).
            on('click', () => markerCLick(town, marker)); //Luodaan karttaan klikattavat markkerit
        if (town[3] === playerLocation) { //Asetetaan kartta pelaajan paikalle
            map.setView([town[0], town[1]], 6);
            playerLocationName = town[2];  //Location name ja päivitetään se stat ruudulle
            marker.setIcon(greenIcon);
            gameScreenText();
        }
    }
}

//Haetaan statsit ja päivitetään ne ruudulle
async function getStats(username) {
    const response = await fetch(`http://127.0.0.1:3000/getstats/${username}`);
    const jsonData = await response.json();
    playerName = jsonData.name;
    playerLocation = jsonData.location;
    playerBanditsCaptured = jsonData.banditsArrested;
    playerTravelMiles = jsonData.travelKm * 0.62;
    playerCurrency = jsonData.money;
    playerDeathCount = jsonData.deathCount;
    gameScreenText();
}

//Pelin alustus funktio
async function gameBegin(evt) {
    evt.preventDefault();
    const username = document.querySelector('#username').value;
    await fetch(`http://127.0.0.1:3000/play/${username}`);
    await getStats(username); //Haetaan statsit ja asetetaan ne näkyviin
    await getWeather(); //Haetaan sää pelin alustusta varten
    getLocations(); //Ladataan pelin kartta ja markkerit
    loginScreen.style.display = 'none';
    gameScreen.style.display = 'flex'; //Gamescreen element näkyviin
}
//Pelin lataus, pelaaja syöttää usernamen, backend lataa tai luo uuden
loadUserForm.addEventListener('submit', gameBegin);


// How to Play button dropdown
gameHelpButton.addEventListener('click', function() {
    if (dropdown.style.display === 'none' || dropdown.style.display === '') {
        dropdown.style.display = 'block';
    } else {
        dropdown.style.display = 'none';
    }
});

// Leaderboard button
leaderboardDropdown();
gameLeaderboardButton.addEventListener('click', function() {
    if (gameLeaderboardDropdown.style.display === 'none' || gameLeaderboardDropdown.style.display === '') {
        gameLeaderboardDropdown.style.display = 'block';
    } else {
        gameLeaderboardDropdown.style.display = 'none';
    }
});

// AUDIO ja GAMESOUNDS
// game soundtrack
function playSoundtrack() {
    soundtrack = new Audio('../sounds/soundtrack.mp3');
    soundtrack.loop = true;
    soundtrack.autoplay = true;
    soundtrack.volume = 0.25;
}

// toggle mute funktio
function toggleMute(audio) {
    const muteIcon = document.querySelector('#mute-icon');
    if (audio.muted) {
        audio.muted = false;
        muteIcon.src = '../images/volume.png';
        muteIcon.alt = 'unmute';
    } else {
        audio.muted = true;
        muteIcon.src = '../images/mute.png';
        muteIcon.alt = 'mute';
    }
}
// mutenappula ja volumebar näkyvyys eventlistener
const muteButton = document.querySelector('#mute-button');
muteButton.innerHTML = '<img id="mute-icon" src="../images/volume.png" alt="mute button">';
muteButton.addEventListener('click', () => toggleMute(soundtrack));
muteButton.addEventListener('mouseover', () => {
    document.querySelector('#volume-control').style.display = 'block';
});
muteButton.addEventListener('mouseout', () => {
    document.querySelector('#volume-control').style.display = 'none';
});

// volumebar säätö ja näkyvyys eventlistener
function volumeBar(audio) {
    audio.volume = +volumeControl.value / 100;
}
const volumeControl = document.querySelector('#volume-control');
volumeControl.min = 0;
volumeControl.max = 50;
volumeControl.value = 25;
volumeControl.addEventListener('input', () => volumeBar(soundtrack));
volumeControl.addEventListener('mouseover', () => {
    document.querySelector('#volume-control').style.display = 'block';
});
volumeControl.addEventListener('mouseout', () => {
    document.querySelector('#volume-control').style.display = 'none';
});

// Kutsutaan soundtrackia
playSoundtrack();


//Event popup sulkemis nappi
eventPopupCloseButton.addEventListener('click', eventPopupClose);


