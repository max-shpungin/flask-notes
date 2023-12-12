import os

from flask import Flask, render_template, redirect, session, flash
from flask_debugtoolbar import DebugToolbarExtension

from models import connect_db, db, User
from forms import RegisterForm, LoginForm

app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = os.environ.get(
    "DATABASE_URL", "postgresql:///flask_notes")
app.config["SQLALCHEMY_ECHO"] = True
app.config["SECRET_KEY"] = "abc123"

connect_db(app)
db.create_all()

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

    if form.validate_on_submit():
        username = form.username.data
        password = form.password.data
        email = form.email.data
        first_name = form.first_name.data
        last_name = form.last_name.data

        user = User.register(username, password, email, first_name, last_name)
        db.session.add(user)
        db.session.commit()

        session["username"] = username

        return redirect(f"/users/{username}")
    else:
        return render_template("register_user.html", form=form)

@app.route("/login", methods=["GET","POST"])
def login_user_form():
    """ Display user login form """

    form = LoginForm()

    if form.validate_on_submit():
        name = form.username.data
        pwd = form.password.data

        user = User.authenticate(name, pwd)

        if user:
            session["username"] = name
            return redirect(f"/app/{name}")

        else:
            form.username.errors = ["nuh uh"]

    return render_template("login_user.html", form=form)

@app.get('/users/<str:username>')
def show_user_detail(username):
    ...
