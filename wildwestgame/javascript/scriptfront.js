//Backend yhteys on 127.0.0.1:3000 kautta
//Endpointit määritetään tähän
'use strict';

const loadUserForm = document.querySelector('#usernameform')
loadUserForm.addEventListener('submit', async function(evt) {
        evt.preventDefault();
        const username = document.querySelector('input').value;
        const response = await fetch(`http://127.0.0.1:3000/load/${username}`);
        const jsonData = await response.json();
        console.log(jsonData)
});
