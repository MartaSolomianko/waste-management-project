"""Server for waste management app."""

from flask import Flask, render_template, request, flash, session, redirect, jsonify
from model import connect_to_db, db
from argon2 import PasswordHasher
from jinja2 import StrictUndefined
from datetime import date, datetime
import crud
import model

app = Flask(__name__)
app.secret_key = "dev"
app.jinja_env.undefined = StrictUndefined
ph = PasswordHasher()


####################### HOMEPAGE/LOGIN/LOGOUT/REGISTER/SEARCH ROUTES ##################

@app.route("/")
def homepage():
    """View homepage."""

    session_user_id = session.get("user_id")

    if session_user_id:
        return redirect("/profile")

    return render_template("homepage.html")
    


@app.route("/register", methods=["POST"])
def register_user():
    """Register a new user."""

    user_email = request.form.get("email")
    user_password = request.form.get("password")
    user_name = request.form.get("name")

    # check that user does not exist in db
    user = crud.get_user_by_email(user_email)

    # if user exists in db, tell them to login
    if user:
        flash("That email already exists, try logging in")
        return redirect("/")
    
    # if user does not exist in db yet, add and commit their info to db
    else:
        # but first check if they entered in a password
        if not user_password:
            flash("Please enter in a password")
            return redirect ("/")
        else:
            hashed_pw = ph.hash(user_password)
            new_user = crud.create_user(user_email, hashed_pw, user_name)
            model.db.session.add(new_user)
            model.db.session.commit()

            # get the new user from the db 
            new_user = crud.get_user_by_email(user_email)

            #add the new users id to the session
            session["user_id"] = new_user.user_id
            
            # flash a message saying Welcome, _____!
            flash(f"Welcome, {new_user.name}!")

            # send the new user to their profile page 
            return redirect ("/profile")

        

@app.route("/login", methods=["POST"])
def login():
    """Process user login."""

    # get user email and password from Login form
    user_email = request.form.get("email")
    password = request.form.get("password")

    # query db for user, if no user will return None, if user will return user object
    user = crud.get_user_by_email(user_email)
    
    # if query returns None, redirect to try signing in again
    if not user:
        flash("That email does not exist!")
        return redirect("/")

    # if user in db, check that their password is correct
    else:
        try: 
            ph.verify(user.password, password)
        except:
            flash(f"{user.email}, check your password")
            return redirect("/")
        
        # if their password is correct, store their user_id in session 
        session["user_id"] = user.user_id
       
        # welcome them back using their email from the Login Form
        flash(f"Welcome back, {user.name}!")

        # take them to their profile page with ID from session
        return redirect("/profile")
    

    
@app.route("/profile/logout")
def user_logout():
    """Process user logout."""

    session.clear()

    return redirect("/")



##################### User Profile Routes ############################################

@app.route("/profile")
def user_profile():
    """Show user's profile page."""

    # getting the user's user_id from session, returns None if no user_id
    session_user_id = session.get("user_id")

    # if there is no user_id in the session, ask the user to Login
    if not session_user_id:
        flash("Please Login")
        return redirect("/")

    # querying the db with the user_id stored in session
    user = crud.get_user_by_id(session_user_id)

    # returns a list of the user's records
    records = crud.get_records_by_user_id(session_user_id)

    # if the user has records, find the date of the first record
    # this is to contextualize the total waste a user has logged
    # if records:

    #     first_record = records[0]
    #     # check that is the first record a user made by looking through record_ids
    #     for record in records:
    #         # find the earliest record_id, this will match the first record a user made
    #         if record.record_id < first_record.record_id:
    #             first_record = record
    
    #     # this is a string
    #     start_date = first_record.date_time
    
    # returns a list of current month's user records
    # using the user_id stored in session and the date stored in session
    # current_records = crud.get_records_by_user_id_for_current_month(session_user_id, today)

    # for record in current_records:
    #     date = record.date_time
    #     date = date.split()
    #     month = date[0]
    #     year = date[2]
        

    return render_template("profile.html", user=user,   
                                        records=records)


####################### SEARCH AN ITEM TO ADD #######################################
@app.route("/profile/search")
def user_item_search():
    """Show search page to user."""

    # getting the user's user_id from session, returns None if no user_id
    session_user_id = session.get("user_id")

    # if there is no user_id in the session, ask the user to Login
    if not session_user_id:
        flash("Please Login")
        return redirect("/")

    return render_template("search.html")


## FIGURE OUT WHAT TO DO WITH RETURN REDIRECT NOW THAT SWITCHED TO JSON
@app.route("/profile/search-item.json", methods=["POST"])
def search():
    """Show search results."""

    # saving search form inputs to variable 
    # user_input = request.args.get("q")

    # grab input from search form in jsx file? 
    user_input = request.json.get("name")
    print()
    print(user_input)

    # accounting for odd characters, capital letters, or blank spaces in search
    search = crud.clean_user_search(user_input)

    # if empty input submitted
    if search == "":
        flash("Sorry, couldn't find that. Try searching again.")
        return redirect("/profile/search/error")
    
    # check if there is an exact name match in db
    item = crud.get_item_by_name(search)

    # check if you can return a result based on a material in db
    if not item:
        item = crud.get_item_by_material(search)

        # if there are no exact matches, check if there is a similar name match in db
        if not item:
            item = crud.get_similar_item_by_name(search)

            # check if there is a similar sounding material in db
            if not item:
                item = crud.get_similar_item_by_material(search)
                
                # if you can't find an item, flash an error message
                if not item:
                    flash(f"Sorry, {search} is not in our database. Try searching for something else.")
                    return redirect("/profile/search/error")


    print()                               
    print("This is the item found in the db")
    print(item.weight)
    print(item.name)
    print(item.bin_type_code)
    print(item.item_id)
    print('############################')

    name = item.name
    weight = item.weight
    bin = item.bin_type_code
    material = item.material

    
    # return render_template("search.html", item=item)
    return jsonify({'name': name, 'weight': weight, 'bin': bin, 'material': material})



@app.route("/profile/search/error")
def search_error():
    """Show error message on search results page if no item is found."""

    item = None

    return render_template("search.html", item=item)



########################## ADD A RECORD ##############################################
@app.route("/profile/add-record.json", methods=["POST"])
def add_record():
    """Add waste record to user's profile page."""

    # connect to formInputs in JS file
    user_id = request.json.get("userid")
    bin_type_code = request.json.get("bintype")
    date_time = request.json.get("datetime")
    weight = request.json.get("weight")
    # print(date_time)
    # print(type(date_time))

    # convert values to the accepted value types for record table in db
    weight = float(weight)
    user_id = int(user_id)

    # keep this format because JS is returning a full date and time stamp
    format = "%Y-%m-%dT%H:%M:%S.%fZ"

    # discarding all of the time info and translating to datetime for python
    date_time = datetime.strptime(date_time, format).date()
    # user_id is a string
    # bin_type_code is a string

    # create record and add it to the db
    new_record = crud.create_record(user=user_id, bin_type=bin_type_code, date_time=date_time, weight=weight)
    db.session.add(new_record)
    db.session.commit()

    print()
    print()
    print("***************")
    print(new_record.record_id)

    record_id = new_record.record_id

    print(record_id)
    
 
    
    # this dictionary goes to .then in JS file and eventually gets inserted back into the html file
    # return jsonify(new_record)
    return jsonify({'weight': weight, 'bintype': bin_type_code, 'datetime': date_time.strftime("%Y-%m-%d"), 'userid': user_id, 'record_id': new_record.record_id})



##################################################################################
#TODO: 
## decide if pie chart should show records from the current year? 
## if a user clicks on a slice from the pie chart, show those records?
## make routes to allow a user to edit a record
################################################################################## 

@app.route("/profile/records_by_user.json")
def get_records_by_user():
    """Get all the records a User has made to show in chart.js pie chart."""

    # get user id from session
    session_user_id = session.get("user_id")
    
    # query the db for all the records that belong to that user id
    # returns a list of records
    records = crud.get_records_by_user_id(session_user_id)
    
    if not records:
        return redirect("/profile")

    # get the total weight of trash
    trash = 0
    # get the total weight of recycling
    recycling = 0
    # get the total weight of compost
    compost = 0
    # get the total weight of hazardous
    hazard = 0

    for record in records:
        if record.bin_type_code == 'T':
            trash += record.weight
        elif record.bin_type_code == 'R':
            recycling += record.weight
        elif record.bin_type_code == 'C':
            compost += record.weight
        else: 
            hazard += record.weight
    
    weight_totals = {"trash": trash, 
                    "recycling": recycling, 
                    "compost": compost, 
                    "hazard": hazard}

    return jsonify(weight_totals)



@app.route("/profile/show-total.json")
def show_total():
    """Show total waste produced by user on profile."""

    # get user id from session
    session_user_id = session.get("user_id")
    
    # returns a list of the user's records
    records = crud.get_records_by_user_id(session_user_id)

    total_weight = 0
    
    for record in records:
        total_weight += record.weight

    return jsonify(total_weight)



@app.route("/profile/show-record.json", methods=["POST"])
def show_record():
    """Get a specific record's information to show in modal on user profile."""

    # get record id from JS file
    record_id = request.json.get("record_id")


    print()
    print("this is the record id:")
    print(record_id)
    print(type(record_id))
    print()

    record_id = int(record_id)

    record = crud.get_record_by_record_id(record_id)
    print()
    print("RECORD ######*************    ##########")
    print(record)
    date = record.date_time
    weight = record.weight
    bin_type_code = record.bin_type_code

    record_info = {"date": date, "weight": weight, "bin_type_code": bin_type_code, "record_id": record_id}
    
    return jsonify(record_info)



@app.route("/profile/delete-record.json", methods=["POST"])
def delete_record():
    """Remove a record from the db and user profile page."""

    record_id = request.json.get("record_id")

    record_id = int(record_id)

    record = crud.get_record_by_record_id(record_id)
    db.session.delete(record)
    db.session.commit()

    return "Record has been removed."



###################################################################
if __name__ == "__main__":
    connect_to_db(app)
    app.run(host="0.0.0.0", debug=True)