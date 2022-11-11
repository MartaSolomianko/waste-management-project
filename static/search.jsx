// React for search page //

//parent component
function SearchForm() {

    // state variables 
    const [name, setName] = React.useState('');
    const [material, setMaterial] = React.useState('');
    const [bin, setBin] = React.useState('');
    const [weight, setWeight] = React.useState(0); 

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
                console.log("inside of fetch request");
                console.log(itemDetails.name);
                setName(itemDetails.name);
                setBin(itemDetails.bin);
                setWeight(itemDetails.weight);
                setMaterial(itemDetails.material);

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
    {bin && <SearchResults name={name} bin={bin} weight={weight} material={material}/>}
    </React.Fragment>
    );
}



// child component
function SearchResults({name, material, bin, weight}) {

    // to pass info from parent to child as props -- material, bin type


    const handleAddRecord = () => {
        console.log('Hi, I added a record')
        // JS line of code this would send back to user profile 
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
    <h3>I am the search results</h3>
    <div>
    <p> Item name: {name} </p>
    <p> Item material: {material} </p>
    <p> Throw this out in: {bin} </p>
    <p> {weight} lbs</p>
    <button onClick={handleAddRecord}>Add to your Records</button>
    </div>
    {/* button will take the user back to their profile page 
    and add a record to the records */}

    {/* add weight form here? */}

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