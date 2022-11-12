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
                console.log("after fetch request");
                console.log(itemDetails.name);
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
    <label htmlFor="searchItem">
    <input 
    value={name} 
    onChange={(event) => setName(event.target.value)} 
    id="searchItem"
    placeholder="Look up an item">
    </input>
    </label>
    <button onClick={handleSubmit}>Enter</button>
    { error && <div> {error} </div> }
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

        const url = `/profile/search/add-record?weight=${userWeight}&bin=${bin}`
        // console.log(url);
        window.location.href = url 
    }

    return (
    <React.Fragment>
    <h3>Search results:</h3>
    <div>
    <p> Item name: {name} </p>
    <p> Item material: {material} </p>
    <p> {name} normally weighs {typicalWeight} lbs</p>

    {/* TODO: play around with the initial value showing up in the input box */}
    <label>Add 
    <input 
    value={userWeight}
    onChange={(event) => setUserWeight(event.target.value)}>
    </input> lbs
    </label>

    {/* button will take the user back to their profile page 
    and add a record to the records */}
    <div>
    <button onClick={handleAddRecord}>{userWeight}lbs to my {bin}</button>
    </div>

    </div>
    </React.Fragment>
    );
}



// grandparent component
function SearchPageContainer() {

    return (
    <React.Fragment>  
    <h2>Search Page!</h2>
    <SearchForm />
    </React.Fragment> 
    );
}


ReactDOM.render(<SearchPageContainer />, document.querySelector('#search-page'));