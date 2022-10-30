"use strict";


////////////////////// ADD RECORD TO USER PROFILE ///////////////////////////////////

// capturing the form id we want to listen for a submission on 
const form = document.querySelector('#addrecord');

// when the submit button is hit on the html form, the callback function is called
function formSubmit(evt) {
    evt.preventDefault();

    // capturing inputs from HTML form
    const formInputs = {
        weight: document.querySelector('#weight').value,
        userid: document.querySelector('#user-id').value,
        bintype: document.querySelector('#bin-type').value,
        datetime: new Date(),

    };

    // connecting to Flask route in Python file
    fetch('/profile/add-record', {
        method: 'POST',
        body: JSON.stringify(formInputs),
        headers: {
          'Content-Type': 'application/json',
        },
    })

    // at this point the Flask route has added the form inputs to the db
    // and returned the infomation it added to the db here as a json response
    // we then take that response, unpack it and 
    // insert those values back into our html user profile page. 
        .then((response) => response.json())
        .then(userRecord => {
            const showRecord = document.querySelector('#display-record');
            showRecord.insertAdjacentHTML('beforeend', `<div><p>Bin Type- ${userRecord.bintype} Weight- ${userRecord.weight} Date- ${userRecord.datetime}</p></div>`);
        });
}

// listening for a submit from the form in our html file
form.addEventListener('submit', formSubmit);
    
