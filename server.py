"""Server for waste management app."""

from flask import Flask, render_template, request, flash, session, redirect
from model import connect_to_db
import crud

from jinja2 import StrictUndefined

app = Flask(__name__)
app.secret_key = "dev"
app.jinja_env.undefined = StrictUndefined


@app.route('/')
def homepage():
    """View homepage."""

    return render_template('homepage.html')



@app.route("/login", methods=["POST"])
def login():
    """Process user login."""

    # get user email and password from login form
    user_id = request.form.get("email")
    password = request.form.get("password")

    # get user_id from the db
    user = crud.get_user_by_id(user_id)




###################################################################
if __name__ == "__main__":
    connect_to_db(app)
    app.run(host="0.0.0.0", debug=True)