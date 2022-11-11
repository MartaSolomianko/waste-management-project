// React for search page //

//parent component
function SearchForm() {

    // state variables 
    const [name, setName] = React.useState('');
    const [material, setMaterial] = React.useState('');
    const [bin, setBin] = React.useState('');
    const [weight, setWeight] = React.useState(0); 
    const [displayName, setdisplayName] = React.useState('');

    // function to maybe update the weight after a user types in a value in the Search results...
    function handleWeight() {
        setWeight()
    }


    // this only happens after the enter button is clicked
    const handleSubmit = (event) => {
        event.preventDefault();
        console.log('Before fetch request'); 
        console.log(name);  

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
                // check for the empty dictionary if empty don't do anything
                console.log("after fetch request");
                console.log(itemDetails.name);
                // setName(itemDetails.name);
                setdisplayName(itemDetails.name);
                setWeight(itemDetails.weight);
                setMaterial(itemDetails.material);
                if (itemDetails.bin === 'R') {
                    setBin('Recycling');
                } else if (itemDetails.bin === 'C') {
                    setBin('Compost');
                } else if (itemDetails.bin === 'T') {
                    setBin('Trash');
                } else {
                    setBin('Hazardous');
                }
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
    {bin && <SearchResults name={displayName} bin={bin} weight={weight} material={material} handleWeight={handleWeight}/>}
    </React.Fragment>
    );
}



// child component
// change weight to typical weight 
// take out the handle weight function
function SearchResults({name, material, bin, weight}) {

    // weight as a state that gets the input a user enters

    const handleAddRecord = (event) => {
        event.preventDefault();
        console.log('Hi, I added a record that weighs:');
        console.log(weight);
        // JS line of code this would send a user back to their user profile page 
        // to add a record to the db I need to send: 
        // datetime
        // weight
        // user_id
        // bin_type_code
        // url = "/add-record?weight=1&material=plastic"
        // window.location.href = url 
    }

    return (
    <React.Fragment>
    <h3>Search results:</h3>
    <div>
    <p> Item name: {name} </p>
    <p> Item material: {material} </p>
    <p> a {name} normally weighs {weight} lbs</p>

    {/* add weight form here? */}
    <label>Add 
    {/* trying to update the prop variable weight back in the parent component */}
    <input onChange={() => handleWeight}></input> lbs
    </label>

    {/* button will take the user back to their profile page 
    and add a record to the records */}
    <div>
    <button onClick={handleAddRecord}>to my {bin}</button>
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