"use strict";

////////////////////////// LOGIN/REGISTER /////////////////////////////
// this section allows a user to toggle back and forth between the 
// login and registration forms on the homepage 

// In login form, capture the don't have an account? Register. span
const registerSpan = document.querySelector('#registration-span');
// // capture register button in nav bar
// const registerButton = document.querySelector('#register-btn');
// In registration form, capture the already have an account? Login. span
const loginSpan = document.querySelector('#login-span')
// // capture login button in nav bar
// const loginButton = document.querySelector('#login-btn')



function showRegister(evt) {

    // hide login form
    document.querySelector('#login-form').hidden = true;
    // show registration form
    document.querySelector('#register-form').hidden = false;
    // // hide registration nav bar button
    // registerButton.hidden = true;
    // // show login nav bar button
    // loginButton.hidden = false;

    }
     
// listen for click on the register span 
registerSpan.addEventListener('click', showRegister);
// // listen for the click on the register button in the nav bar
// registerButton.addEventListener('click', showRegister);



function showLogin(evt) {

    // show login form
    document.querySelector('#login-form').hidden = false;
    // hide registration form
    document.querySelector('#register-form').hidden = true;
    // // show registration nav bar button
    // registerButton.hidden = false;
    // // hide login nav bar button
    // loginButton.hidden = true;

    }
     
// listen for click on the register span 
loginSpan.addEventListener('click', showLogin);
// // listen for the click on the register button in the nav bar
// loginButton.addEventListener('click', showLogin);

