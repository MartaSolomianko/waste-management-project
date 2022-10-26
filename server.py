"""Server for waste management app."""

from flask import Flask, render_template, request, flash, session, redirect
from model import connect_to_db
import crud
import model

from jinja2 import StrictUndefined

app = Flask(__name__)
app.secret_key = "dev"
app.jinja_env.undefined = StrictUndefined


@app.route('/')
def homepage():
    """View homepage."""

    return render_template('homepage.html')



@app.route("/register", methods=["POST"])
def register_user():

    user_email = request.form.get("email")
    user_password = request.form.get("password")

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
            new_user = crud.create_user(user_email, user_password)
            model.db.session.add(new_user)
            model.db.session.commit()
            # get that new user you just committed from the db
            user = crud.get_user_by_email(user_email)
            # flash a message saying Welcome, _____!
            flash(f"Welcome, {user.email}!")
            # redirect to homepage or user profile page? 
            return redirect (f"/profile/{user.user_id}")
    
    
## TODO:    
#### 2. Save user_id to session? 

        

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
        if password != user.password:
            flash(f"{user.email}, check your password")
            return redirect("/")
        # if their password is correct, welcome them back using their email
        flash(f"Welcome back, {user.email}!")
        # take them to their profile page
        return redirect(f"/profile/{user.user_id}")

    
    ## TODO: 
    #### 1. store user ID in session
    #### 2. instead of using the user object from db to make my URL, use client's session
    ## this is for added security so that folks can't just get to a user's profile page by 
    ## guessing their user id in the URL, meaning if their user ID is not stored in their
    ## session, they will not be allowed to go to that profile page. 
    


    

@app.route("/profile/<user_id>")
def user_profile(user_id):
    """Show user's profile page."""

    user = crud.get_user_by_id(user_id)

    return render_template(f"profile.html", user=user)




###################################################################
if __name__ == "__main__":
    connect_to_db(app)
    app.run(host="0.0.0.0", debug=True)