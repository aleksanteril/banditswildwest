//Backend yhteys on 127.0.0.1:3000 kautta
//Endpointit määritetään tähän
'use strict';

async function loadUser(userId) {
        const response = await fetch(`http://127.0.0.1:3000/users/${userId}`);
}

function displayUser(user) {
    const userInfoDiv = document.querySelector('#user-info');
    userInfoDiv.innerHTML = `
        <h2>${user.isNew ? 'New User' : 'Returning User'}</h2>
        <p>Name: ${user.name}</p>`;
}

const userId = 1;
loadUser(userId);