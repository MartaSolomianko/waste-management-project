"use strict";

////////////////////////// LOGIN/REGISTER /////////////////////////////
// this section allows a user to toggle back and forth between the 
// login and registration forms on the homepage 

// In login form, capture the don't have an account? Register. span
const registerSpan = document.querySelector('#registration-span');
// In registration form, capture the already have an account? Login. span
const loginSpan = document.querySelector('#login-span')


function showRegister(evt) {
    // hide login form
    document.querySelector('#login-form').hidden = true;
    // show registration form
    document.querySelector('#register-form').hidden = false;
    }
     
// listen for click on the register span 
registerSpan.addEventListener('click', showRegister);



function showLogin(evt) {
    // show login form
    document.querySelector('#login-form').hidden = false;
    // hide registration form
    document.querySelector('#register-form').hidden = true;
    }
     
// listen for click on the register span 
loginSpan.addEventListener('click', showLogin);


