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


####################### HOMEPAGE/LOGIN/LOGOUT/REGISTER ##############################
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
            # flash(f"Welcome, {new_user.name}!")

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
        # flash(f"Welcome back, {user.name}!")

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

    # reverse the returned records bc I want the most recent month to
    # appear first on the user profile page
    sorted_records = records[::-1]

    # dictionary key contains the month and year
    # value of each key is a list of those records associated with that year and month
    records_dict = {}

    # today's month and year used only when a user does not have records yet for the current month/year
    today = datetime.now().date().strftime("%Y %B")
    
    # opening up the list of a user's record objects 
    for record in sorted_records:
        # sort each record into a list based on date
        record_date = record.date_time.strftime("%Y %B")
        # print()
        # print(record_date)
        if today not in records_dict:
            records_dict[today] = []
        if record_date not in records_dict:
            records_dict[record_date] = []
        records_dict[record_date].append(record)

    # this sorts the dictionary values, aka the records from newest to oldest
    for month_year in records_dict:
        records_dict[month_year] = records_dict[month_year][::-1]

    if records:
        first_record = records[0]
        start_date = first_record.date_time.strftime("%B %d, %Y")
        # print(start_date)

    # if a new user, initailze all values to today and ready for them to begin entering records    
    if not records: 
        start_date = today
        records_dict[today] = []

    return render_template("profile.html", user=user, records_dict=records_dict, start_date = start_date)


####################### SEARCH AN ITEM TO ADD SEARCH IN REACT #######################
@app.route("/profile/search")
def user_item_search():
    """Show search page to user."""

    # getting the user's user_id from session, returns None if no user_id
    # need the user's id in case they want to log a record of an individual item
    session_user_id = session.get("user_id")

    # if there is no user_id in the session, ask the user to Login
    if not session_user_id:
        flash("Please Login")
        return redirect("/")

    return render_template("search.html")



@app.route("/profile/search-item.json", methods=["POST"])
def search():
    """Show search results."""

    # grab input from search form in jsx file 
    user_input = request.json.get("name")
    # print()
    # print(user_input)

    # accounting for odd characters, capital letters, or blank spaces in search
    search = crud.clean_user_search(user_input)

    # if empty input submitted
    if search == "":
        return jsonify({})
    
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
                    return jsonify({})

    # capture the info of the found item
    name = item.name
    weight = item.weight
    bin = item.bin_type_code
    material = item.material
    
    return jsonify({'name': name, 'weight': weight, 'bin': bin, 'material': material})



########################## ADD A RECORD FROM USER PROFILE PAGE ######################
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
    # bin_type_code is a string

    # keep this format because JS is returning a full date and time stamp
    format = "%Y-%m-%dT%H:%M:%S.%fZ"

    # discarding all of the time info and translating to datetime for python
    date_time = datetime.strptime(date_time, format).date()
    # date_time = date(2022,11,28)

    # create record and add it to the db
    new_record = crud.create_record(user=user_id, bin_type=bin_type_code, date_time=date_time, weight=weight)
    db.session.add(new_record)
    db.session.commit()

    # switching bin codes for names to trigger color coding on buttons on user profile
    if bin_type_code == "T":
        bin_type_code = "trash"
    elif bin_type_code == "C":
        bin_type_code = "compost"
    elif bin_type_code == "R":
        bin_type_code = "recycle"
    else: 
        bin_type_code = "hazard"

    # this dictionary goes to .then in JS file and eventually gets inserted back into the html file
    return jsonify({'weight': weight, 'bintype': bin_type_code, 'datetime': date_time.strftime("%d"), 'userid': user_id, 'record_id': new_record.record_id})



#################### ADD A RECORD FROM SEARCH/REACT PAGE ############################
@app.route("/profile/search/add-record")
def add_item_record():
    """Add a record to the db and return a user back to the profile page."""

    ## get values to add to db from query string
    weight = request.args.get("weight")
    bin = request.args.get("bin")

    # switch weight to a integer
    weight = float(weight)

    # switch bin type to a code
    if bin == "Recycling":
        bin = "R"
    elif bin == "Compost":
        bin = "C"
    elif bin == "Trash":
        bin = "T"
    else:
        bin = "H"

    # stamp a record here with datetime.now
    date_time = datetime.now().date()

    # getting the user's user_id from session, returns None if no user_id
    # this is for both loading the profile page and also to add a record to db
    session_user_id = session.get("user_id")

    # if there is no user_id in the session, ask the user to Login
    if not session_user_id:
        flash("Please Login")
        return redirect("/")

    # create record and add it to the db
    new_record = crud.create_record(user=session_user_id, bin_type=bin, date_time=date_time, weight=weight)
    db.session.add(new_record)
    db.session.commit()

    return redirect("/profile")



######### SHOW TOTAL WEIGHTS OF WASTE RECORDS IN USER PROFILE IN PIE CHART ##########
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


################## SHOW TOTAL WEIGHT OF WASTE PRODUCED ON USER PROFILE ################
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



################# SHOW DAILY RATE OF WASTE PRODUCED ON USER PROFILE ##################
@app.route("/profile/show-daily-rate.json")
def show_daily_rate():
    """Show a users daily rate in lbs per day on profile."""

    # get user id from session
    session_user_id = session.get("user_id")
    
    # returns a list of the user's records
    records = crud.get_records_by_user_id(session_user_id)

    # if a user has recorded more than 12 records of waste 
    # chose 12 because I calculated on avg a user would throw out 
    # R, T, C once/week meaning 12 times per month.
    if len(records) >= 12:
        # grabs the first record a user has
        first_record = records[0] 
        # takes the date of that first record
        first_date = first_record.date_time

        # capturing the date today
        today = datetime.now().date()
        # calculating a timedelta instance, aka the difference between two datetime dates
        delta = today - first_date
        # grabbing just the day portion of that timedelta instance
        delta = delta.days

        total_weight = 0

        for record in records:
            total_weight += record.weight

        # calculating the daily rate based total weight produced / total days since first record
        daily_rate = total_weight / delta

    return jsonify(daily_rate)



##################### USER RECORD INFO IN MODAL POP UP ON PROFILE ###################
@app.route("/profile/show-record.json", methods=["POST"])
def show_record():
    """Get a specific record's information to show in modal on user profile."""

    # get record id from JS file
    record_id = request.json.get("record_id")

    record_id = int(record_id)

    # get all info about a particular record using the record id
    record = crud.get_record_by_record_id(record_id)

    # get the record's date from the db and make it into a reader friendly string
    date = record.date_time.strftime("%B %d")

    weight = record.weight
    bin_type_code = record.bin_type_code
    
    # switch bin type to a code
    if bin_type_code == "R":
        bin_type_code = "Recycling"
    elif bin_type_code == "C":
        bin_type_code = "Compost"
    elif bin_type_code == "T":
        bin_type_code = "Trash"
    else:
        bin_type_code = "Hazard"

    record_info = {"date": date, "weight": weight, "bin_type_code": bin_type_code, "record_id": record_id}
    
    return jsonify(record_info)



############ DELETE A RECORD FROM MODAL POP UP ######################################
@app.route("/profile/delete-record.json", methods=["POST"])
def delete_record():
    """Remove a record from the db and user profile page."""

    # get the specific record id from the JS file
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