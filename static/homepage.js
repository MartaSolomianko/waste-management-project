"use strict";

////////////////////////// NAVIGATION BAR /////////////////////////////

// capture register button
const registerButton = document.querySelector('#register-btn');

function showRegister(evt) {

    document.querySelector('#hidden-registration').hidden = false;
    
} 

// listen for register button click
registerButton.addEventListener('click', showRegister);




// capture login button 
const loginButton = document.querySelector('#login-btn');

function showLogin(evt) {

    document.querySelector('#hidden-login').hidden = false;

}

// listen for login button click
loginButton.addEventListener('click', showLogin);
