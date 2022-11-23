"use strict";

///////////////// CHART JS DISPLAY ON USER PROFILE //////////////////////////////////
/////// pie chart that shows a user's lifetime record totals ////////////////////////
// setting chart as a global variable
let ctx 
// get data from Flask route
// data should be a jsonified dict of totals from a user
// then ordered by [Trash, Recycling, Compost, Hazard]
function userChart() {
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

            // Insert pie chart into user profile page at the canvas id #piechart
            ctx = new Chart(document.querySelector('#piechart'), {
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
                    // label: '2022 Waste totals',
                    data: data,
                    backgroundColor: [
                        '#2E2E30',
                        '#037ba0',
                        '#8fa175',
                        '#84031b',
                    ],
                    hoverOffset: 2
                }]
            },  options: {
                    plugins : {
                        title: {
                            display: true,
                            text: 'Waste Totals'
                        }
                    }
                } 
            });
            // .catch method to catch an error msg from the redirect in server route
            // this is because I don't want anything to show up on the profile if 
            // a user doesn't have a record
        }).catch(() => console.log('catching error'));
    }
// get user chart to load with current data from db when profile page is opened
userChart();



////////////////////// ADD RECORD TO USER PROFILE ///////////////////////////////////
/// adds a record to the user's profile when the add record form is submitted ///////

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

    // console.log("This is the new record I want to add to the db:");
    // console.log(formInputs);
    // console.log("This record is a new object and does not have an ID yet")
    // console.log("It will get its ID after it is added to the db")



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

            // console.log("This is the user record I just got back from my Flask route:");
            // console.log(userRecord);
            // console.log("This record is a:");
            // console.log(typeof(userRecord));
            // console.log("It now has a record ID of:");
            // console.log(userRecord.record_id);

            const showUserRecord = document.querySelector('#display-record');
            showUserRecord.insertAdjacentHTML('beforeend', 
            `<div id="record-${userRecord.record_id}" value="${userRecord.record_id}">
            <button class="btn btn-primary modal-btn user-record-btn" data-bs-toggle="modal" data-bs-target="#show-record-modal" value="${userRecord.record_id}">
            <p>${userRecord.bintype}</p>
            <p>Date - ${userRecord.datetime}</p>
            <p>Weight - ${userRecord.weight}</p>
            </button>
            </div>
            `
            );
            

            document.querySelector(`#record-${userRecord.record_id} .user-record-btn`).addEventListener('click', showRecord);

            
            // this allows the pie chart to change dynamically
            // as a user adds their records in the db
            console.log(ctx);

            if (ctx == null) {
                userChart();
                // console.log("We made the chart!");
                showTotalWaste();
            } else {
                ctx.destroy();
                // console.log("Hi we have destroyed the chart but not yet made the chart");
                userChart();
                // console.log("We made the chart");
                showTotalWaste();
                showDailyRate();
            }
            
        });
}

// listening for a submit from the form in our html file
form.addEventListener('submit', formSubmit);



//////////////////// SHOW FULL RECORD IN MODAL POPUP ON USER PROFILE ///////////////
// Shows the full record's info on a user's profile in a modal popup when a record button is clicked //
function showRecord(evt) {
    const id = evt.currentTarget.getAttribute("value");
    // console.log("This is the event.target");
    // console.log(evt.currentTarget);
    // console.log("This is the id of the record I clicked outside of my if statement:");
    // console.log(id);

    if (id !== null) {
        const record = {
            record_id: evt.currentTarget.getAttribute("value"), }
    
        // console.log("This is the record id inside of the if statement:");
        // console.log(record.record_id);
        // console.log(typeof(record.record_id));
        // console.log("This is the event object I have put a target on:");
        // console.log(evt);
    
        
        fetch('/profile/show-record.json', {
            method: 'POST',
            body: JSON.stringify(record),
            headers: {
              'Content-Type': 'application/json',
            },
        })
    
        .then((response) => response.json())
        .then(userRecord => {
            const showRecord = document.querySelector('#show-a-record');
            // console.log("This is the user record:")
            // console.log(userRecord);
            // console.log("This is the date on the record")
            // console.log(userRecord.date);
            showRecord.innerHTML = " ";
            // console.log(typeof(userRecord.date));
            // let date = userRecord.date;
            // console.log(date);
           
            // hidden input here that will be used for when/if a user will want to delete this specific record.
            showRecord.innerHTML = `<div class="modal-title" id="show-record-title" value="${userRecord.record_id}">${userRecord.date}</div>
                                <div id="show-record-weight" value="${userRecord.record_id}">${userRecord.weight} <span id="weight-label">lbs</span></div> 
                                <div id="show-record-bin" value="${userRecord.record_id}">${userRecord.bin_type_code}</div>
                                <input hidden id="delete-record-id" value="${userRecord.record_id}"></input>`;
        });
    }
}

// capture all the records and add an event listener to them 
let buttons = document.querySelectorAll('.user-record-btn');
// console.log("Setting up event handlers for buttons");
    for (const button of buttons) {
        button.addEventListener('click', showRecord);
    }



//////////////////// DELETE A RECORD FROM USER PROFILE AND DB ///////////////////////
const deleteBtn = document.querySelector('#delete-record-btn');

function deleteRecord(evt) {
    evt.preventDefault();

    const deleteRecord = {
        record_id: document.querySelector('#delete-record-id').value, }

    // console.log(deleteRecord);
    // console.log("This is the record ID:");
    // console.log("for the record I want to delete:");
    // console.log(deleteRecord.record_id);
    alert('Are you sure you want to delete this record?');

    fetch('/profile/delete-record.json', {
        method: 'POST',
        body: JSON.stringify(deleteRecord),
        headers: {
          'Content-Type': 'application/json',
        },
    })

    .then((response) => response.text())
    .then(removeResponse => {
        const record = document.querySelector(`#record-${deleteRecord.record_id}`);
        // console.log(record);
        record.remove();
        alert(removeResponse);
        ctx.destroy();
        userChart();
        showTotalWaste();
        showDailyRate();
    });
}

// this delete button is on the modal pop up
deleteBtn.addEventListener('click', deleteRecord);



///////////////// SHOW TOTAL WASTE PRODUCED ON USER PROFILE ///////////////////////
function showTotalWaste() {
    fetch('/profile/show-total.json')
        .then((response) => response.json())
        .then(userTotal => {
            // console.log(typeof(userTotal));
            const showTotal = document.querySelector('#lifetime-total');
            // .toFixed keeps the user total to two decimal places
            userTotal = userTotal.toFixed(2);
            showTotal.innerHTML = `${userTotal} <span id="weight-label">lbs</span>`;
        
        });
    }

showTotalWaste();


/////////////////////// SHOW DAILY RATE ON USER PROFILE ///////////////////////////
function showDailyRate() {
    fetch('/profile/show-daily-rate.json')
    .then((response) => response.json())
    .then(userDailyRate => {

        const showDailyRate = document.querySelector('#daily-rate');
        userDailyRate = userDailyRate.toFixed(2);
        showDailyRate.innerHTML = `${userDailyRate} <span id="weight-label">lbs/day</span>`;
    });
}

showDailyRate();
