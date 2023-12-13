import os

from flask import Flask, render_template, redirect, session, flash
from flask_debugtoolbar import DebugToolbarExtension

from models import connect_db, db, User
from forms import RegisterForm, LoginForm, CSRFProtectForm

#this is a key that stores the username in the session
USERNAME = "username"

app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = os.environ.get(
    "DATABASE_URL", "postgresql:///flask_notes")
app.config["SQLALCHEMY_ECHO"] = True
app.config["SECRET_KEY"] = "abc123"
app.config['DEBUG_TB_INTERCEPT_REDIRECTS'] = False

connect_db(app)

toolbar = DebugToolbarExtension(app)


@app.get("/")
def redirect_to_register():
    """Redirect to /register
    """

    return redirect("/register")

@app.route("/register", methods=["GET", "POST"])
def register_user_form():
    """Display register user form"""

    form = RegisterForm()

    # check if logged in then take to user page, shouldn't be allowed to go to register page while logged in
    if form.validate_on_submit():
        username = form.username.data
        password = form.password.data
        email = form.email.data
        first_name = form.first_name.data
        last_name = form.last_name.data

        user = User.register(username, password, email, first_name, last_name)
        db.session.add(user)
        db.session.commit()

        session[USERNAME] = user.username

        return redirect(f"/users/{username}")
    else:
        return render_template("register_user.html", form=form)

@app.route("/login", methods=["GET","POST"])
def login_user_form():
    """ Display user login form """

    # check if logged in then take to user page, shouldn't be allowed to go to login page while logged in

    form = LoginForm()

    if form.validate_on_submit():
        name = form.username.data
        pwd = form.password.data

        user = User.authenticate(name, pwd)

        if user:
            session[USERNAME] = user.username
            return redirect(f"/users/{user.username}")

        else:
            form.username.errors = ["nuh uh"]

    return render_template("login_user.html", form=form)

@app.get('/users/<username>')
def show_user_detail(username):
    """Display user details"""

    user = User.query.get_or_404(username)
    form = CSRFProtectForm()

    #if username in session
    if session.get("username") == username:
        return render_template("user_detail.html", user=user, form=form)
    else:
        flash("You are not authorized to view this page")
        return redirect("/register")

@app.post('/logout')
def logout():
    """Logout of the user's session"""

    form = CSRFProtectForm()

    # if doesn't validate on submit, raise Unauthorized method

    if form.validate_on_submit():
        session.pop(USERNAME, None)
    return redirect("/login")