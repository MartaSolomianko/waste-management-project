"use strict";


////////////////////// ADD RECORD TO USER PROFILE ///////////////////////////////////

function submitRecord(evt) {
    evt.preventDefault();

    //get the values from the form with the specific #id input fields
    const formInputs = {
        user_id: document.querySelector('#').value, //where does the user_id come from? 
        bin_type_code: document.querySelector('#bin-type-code').value,
        date_time: document.querySelector('#').value, //how do I capture date-time on submit?
        weight: document.querySelector('#weight').value,
    };

    fetch('/add-record', {
        method: 'POST',
        body: JSON.stringify(formInputs),
        headers: {
          'Content-Type': 'application/json',
        },
      })

    .then((response) => response.json())
    .then(userRecord => {
        /// find id of where to insert the user's new record document.querySelector()
        // and perhaps use .insertAdjacentHTML 
    })
}



// capture the #add-record form and listen for submit
document.querySelector('#add-record').addEventListener('submit', submitRecord)