// React for search page //

//parent component
function SearchForm() {

    // state variables 
    const [name, setName] = React.useState('');
    const [material, setMaterial] = React.useState('');
    const [bin, setBin] = React.useState('');
    const [typicalWeight, setTypicalWeight] = React.useState(0); 
    const [displayName, setDisplayName] = React.useState('');
    const [error, setError] = React.useState('');


    // this only happens after the enter button is clicked
    const handleSubmit = (event) => {
        event.preventDefault();
        // console.log('Before fetch request'); 
        // console.log(name);  

        // sending the input the user typed into the search route in server.py
        fetch('/profile/search-item.json', {
            method: 'POST',
            body: JSON.stringify({name}),
            headers: {
                'Content-Type': 'application/json',
            },    
        })
            .then((response) => response.json())
            .then((itemDetails) => {
                // check for the empty dictionary if empty, show error message
                if (Object.keys(itemDetails).length === 0) {
                    // console.log("Try searching again!");
                    // set search results to not show up on the page
                    setDisplayName('');
                    setError('We could not find that, try searching again.');
                    // console.log(error);

                } else {
                setError('');
                // console.log("after fetch request");
                // console.log(itemDetails.name);
                // setName(itemDetails.name);
                setDisplayName(itemDetails.name);
                setTypicalWeight(itemDetails.weight);
                setMaterial(itemDetails.material);
                if (itemDetails.bin === 'R') {
                    setBin('Recycling');
                } else if (itemDetails.bin === 'C') {
                    setBin('Compost');
                } else if (itemDetails.bin === 'T') {
                    setBin('Trash');
                } else {
                    setBin('Hazardous');
                }}
            });
    }     
    return (
    <React.Fragment>
    <form className="search-form">
    <label htmlFor="searchItem"></label>
        <input 
        value={name} 
        className="search-input"
        onChange={(event) => setName(event.target.value)} 
        id="searchItem"
        placeholder="What are you throwing out?">
        </input>
    <button className="search-btn" onClick={handleSubmit}>Enter</button>
    </form>
    {/* if there is an error message for a search not found in db, this allows the error to appear on page */}
    { error && <div className="err-msg"> {error} </div> }
    {/* using display name becuase I did not want the search results to appear on the page until a user clicks the enter button */}
    { displayName && <SearchResults name={displayName} bin={bin} typicalWeight={typicalWeight} material={material}/>}
    </React.Fragment>
    );
}



// child component
function SearchResults({name, material, bin, typicalWeight}) {

    // this stores the weight input a user enters
    const [userWeight, setUserWeight] = React.useState('');

    const handleAddRecord = (event) => {
        event.preventDefault();
        // console.log('Hi, I added a record that weighs:');
        // console.log(typicalWeight);
        // console.log(userWeight);

        // passing back the info a user entered to server.py in a query string
        // this is because I wanted to bring the user back to their profile page
        // and adjust their totals based on what they entered in here. 
        const url = `/profile/search/add-record?weight=${userWeight}&bin=${bin}`
        // console.log(url);
        window.location.href = url 
    }

    return (
    <React.Fragment>
    {/* Search results and form to log an individual item's weight to a bin */}
        <div id="search-results-card" className="card">
            <div id="search-result-title"> {name} </div>
            {/* <p> Item material: {material} </p> */}
            <p id="search-description"> 1 {name} typically weighs {typicalWeight} lbs</p>
            {/* this is the form to add a weight to a user's bin in the db */}
            <form id="log-item-form">
            <label htmlFor="logWeight"></label>
            <input 
            value={userWeight}
            placeHolder="Weight in pounds"
            className="log-item-weight-input"
            onChange={(event) => setUserWeight(event.target.value)}>
            </input><span id="lbs-label"> lbs</span>
            {/* this button will take the user back to their profile page 
            and add a record to their records */}
            <button className="log-item-btn" onClick={handleAddRecord}>Log <span id="log-item-lbs-label">{userWeight} lbs</span> to my {bin}</button>
            </form>
        </div>
    </React.Fragment>
    );
}



// grandparent component
function SearchPageContainer() {

    return (
    <React.Fragment>  
    {/* <h2>Search Page!</h2> */}
    <SearchForm />
    </React.Fragment> 
    );
}


ReactDOM.render(<SearchPageContainer />, document.querySelector('#search-page'));