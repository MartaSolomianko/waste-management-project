"use strict";


////////////////////// ADD RECORD TO USER PROFILE ///////////////////////////////////

// capturing the form id we want to listen for a submission on 
const form = document.querySelector('#addrecord');

// when the submit button is hit on the html form, the callback function is called
function formSubmit(evt) {
    evt.preventDefault();

    // capturing inputs from HTML form and including a date and time stamp 
    const formInputs = {
        weight: document.querySelector('#weight').value,
        userid: document.querySelector('#user-id').value,
        bintype: document.querySelector('#bin-type').value,
        datetime: new Date(),

    };

    // console.log(formInputs.datetime)

    // connecting to Flask route in Python file
    fetch('/profile/add-record.json', {
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
            showRecord.insertAdjacentHTML('beforeend', `<div><p>Date - ${userRecord.datetime} Bin Type- ${userRecord.bintype} Weight- ${userRecord.weight}</p></div>`);
        });
}

// listening for a submit from the form in our html file
form.addEventListener('submit', formSubmit);
    



////////////////////////////// CHART JS DISPLAY ON USER PROFILE /////////////////////
// get data from Flask route
// data should be a jsonified dict of totals from current year
// ordered by [Trash, Recycling, Compost, Hazard]
fetch('/profile/records_by_user.json')
    .then((response) => response.json())
    .then(userRecords => {
        // console.log(userRecords);
        // console.log(typeof(userRecords.trash));

        const data = [userRecords.trash, 
                        userRecords.recycling, 
                        userRecords.compost, 
                        userRecords.hazard];

        // console.log(data)

        // Insert pie chart into user profile page at the canvas id #testChart
        new Chart(document.querySelector('#pieChart'), {
            type: 'pie',
            data: {
                labels: [
            'Trash',
            'Recycling',
            'Compost',
            'Hazard'
            ],
            datasets: [{
                // not clear as to where this label shows up 
                label: '2022 Waste totals',
                data: data,
                backgroundColor: [
                    'rgb(255, 99, 132)',
                    'rgb(54, 162, 235)',
                    'rgb(255, 205, 86)',
                    'rgb(2, 20, 186)',
                ],
                hoverOffset: 2
            }]
          }
        });
    });
