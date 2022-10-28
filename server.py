"""Server for waste management app."""

from flask import Flask, render_template, request, flash, session, redirect
from model import connect_to_db
from argon2 import PasswordHasher
import crud
import model

from jinja2 import StrictUndefined

app = Flask(__name__)
app.secret_key = "dev"
app.jinja_env.undefined = StrictUndefined
ph = PasswordHasher()


@app.route("/")
def homepage():
    """View homepage."""

    return render_template("homepage.html")


########################################################################
###TODO for Search:

# edge cases: 
# longer searches (i.e. break them down into one word searches)
# account for blank input. Use crud.check_search_not_empty()

# put entire search in a loop(s) to minimize repetitive if statements
# account for search appearing on other pages...
#########################################################################

@app.route("/search")
def search():
    """Show search results."""

    # saving search form inputs to variable 
    user_input = request.args.get("q")

    # accounting for odd characters, capital letters, or blank spaces in search
    search = crud.clean_user_search(user_input)

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
                    flash("We couldn't find that, try searching again.")
                    return redirect("/")
    
    return render_template("search.html", item=item)



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

    return render_template("profile.html", user=user)



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



###################################################################
if __name__ == "__main__":
    connect_to_db(app)
    app.run(host="0.0.0.0", debug=True)