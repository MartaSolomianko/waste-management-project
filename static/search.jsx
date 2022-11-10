// React for search page //

// state variables
// name
// material
// bin
// weight


//parent component
function SearchForm() {

    // state variables 
    const [name, setName] = React.useState('');
    const [material, setMaterial] = React.useState('');
    const [bin, setBin] = React.useState('');
    const [weight, setWeight] = React.useState(0); 


    const handleSubmit = () => {
        console.log('Hi, I searched for something'); 
        setName('plastic bottle');

        // child component SearchResults

    }

    // fetch request to update, material, bin type here? 

    return (
    <React.Fragment>
    <h3>I am the search form</h3>
    <button onClick={handleSubmit}>Search</button>
    <SearchResults name={name}/>
    </React.Fragment>

    );
}



// child component
function SearchResults(props) {

    // to pass info from parent to child as props -- material, bin type

    const handleAddRecord = () => {
        console.log('Hi, I added a record')
        // JS line of code this would send back to user profile 
        // url = "/add-record?weight=1&material=plastic"
        // window.location.href = url 

    }

    return (
    <React.Fragment>
    <h3>I am the search results</h3>
    <p> {props.name} </p>
    <button onClick={handleAddRecord}>Add to your Records</button>
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