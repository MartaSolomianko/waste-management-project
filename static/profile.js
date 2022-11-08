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
                        'rgb(255, 99, 132)',
                        'rgb(54, 162, 235)',
                        'rgb(255, 205, 86)',
                        'rgb(2, 20, 186)',
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

    console.log(formInputs.datetime);
    console.log(typeof(formInputs.datetime));

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

            console.log(userRecord);
            console.log(typeof(userRecord));
            const showRecord = document.querySelector('#display-record');
            showRecord.insertAdjacentHTML('beforeend', 
            `<div id="record-${userRecord.recordid}">
            <button id="user-record-btn" class="btn btn-primary modal-btn" data-bs-toggle="modal" data-bs-target="#show-record-modal" value="${userRecord.recordid}">
            <p>${userRecord.bintype}</p>
            <p>Date - ${userRecord.datetime}</p>
            <p>Weight - ${userRecord.weight}</p>
            </button>
            </div>
            `
            );
            
            // this allows the pie chart to change dynamically
            // as a user adds their records in the db
            ctx.destroy();
            userChart();
            showTotalWaste();
        });
}

// listening for a submit from the form in our html file
form.addEventListener('submit', formSubmit);



//////////////////// SHOW FULL RECORD IN MODAL POPUP ON USER PROFILE ///////////////
/////// Shows the full record on a user's profile when a record button is clicked //
function showRecord(evt) {
    const id = evt.target.getAttribute("value")
    if (id !== null) {
        const record = {
            recordid: evt.target.getAttribute("value"), }
    
        console.log("This is the event object:");
        console.log(evt);
    
        console.log("This is the record id:");
        console.log(record.recordid);
        console.log(typeof(record.recordid));
        
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
            showRecord.innerHTML = " ";
            // console.log(typeof(userRecord.date));
            // let date = userRecord.date;
            // console.log(date);
           
            showRecord.innerHTML = `
                                <p value="${userRecord.recordid}">${userRecord.date}</p>
                                <p value="${userRecord.recordid}">${userRecord.weight} lbs</p> 
                                <p value="${userRecord.recordid}">${userRecord.bin_type_code}</p>
                                <input hidden id="delete-record-id" value="${userRecord.recordid}"></input>`;
        });
    }
}

// capture all the records and add an event listener to them 
let buttons = document.querySelectorAll('.user-record-btn');
const buttonsFromNodeList = Array.from(buttons);

buttonsFromNodeList.forEach(button => button.addEventListener('click', showRecord));
// for (const button of buttons) {
//     button.addEventListener('click', showRecord);
// }



//////////////////// DELETE A RECORD FROM USER PROFILE AND DB ///////////////////////
const deleteBtn = document.querySelector('#delete-record-btn');

function deleteRecord(evt) {
    evt.preventDefault();
    // alert('Are you sure you want to delete this record?');

    const deleteRecord = {
        recordid: document.querySelector('#delete-record-id').value, }

    // console.log(deleteRecord)


    fetch('/profile/delete-record.json', {
        method: 'POST',
        body: JSON.stringify(deleteRecord),
        headers: {
          'Content-Type': 'application/json',
        },
    })

    .then((response) => response.text())
    .then(removeResponse => {
        const record = document.querySelector(`#record-${deleteRecord.recordid}`);
        // console.log(record);
        record.remove();
        alert(removeResponse);
        ctx.destroy();
        userChart();
        showTotalWaste();
    });
}

deleteBtn.addEventListener('click', deleteRecord);



///////////////// SHOW TOTAL WASTE PRODUCED ON USER PROFILE /////////////////////
function showTotalWaste() {
    fetch('/profile/show-total.json')
        .then((response) => response.json())
        .then(userTotal => {
            // console.log(typeof(userTotal));
            const showTotal = document.querySelector('#lifetime-total');
            userTotal = userTotal.toFixed(2);
            showTotal.innerText = `${userTotal} lbs`;
        
        });
    }

showTotalWaste();
