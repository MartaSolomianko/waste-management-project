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

            # for better security, do not use the user object to redirect 
            # the user to their profile page. Instead store their id 
            # in session and use that to send them to their profile page.
            # the route on line 95 /profile now handles this.  
            session["user_id"] = user.user_id
            
            # flash a message saying Welcome, _____!
            flash(f"Welcome, {user.email}!")

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
        if password != user.password:
            flash(f"{user.email}, check your password")
            return redirect("/")
        
        # if their password is correct, store their user_id in session 
        session["user_id"] = user.user_id
       
        # welcome them back using their email from the Login Form
        flash(f"Welcome back, {user.email}!")

        # take them to their profile page with ID from session
        return redirect("/profile")


    
@app.route("/profile")
def user_profile():
    """Show user's profile page."""

    # getting the user's user_id from session, if statement here? 
    session_user_id = session.get("user_id")

    # if there is no user_id in the session, ask the user to Login
    if not session_user_id:
        flash("Please Login")
        return redirect("/")

    # querying the db with the user_id stored in session
    user = crud.get_user_by_id(session_user_id)

    return render_template("profile.html", user=user)




###################################################################
if __name__ == "__main__":
    connect_to_db(app)
    app.run(host="0.0.0.0", debug=True)