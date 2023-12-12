from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt

db = SQLAlchemy()

bcrypt = Bcrypt()

class User(db.Model):
    """ Users !"""

    __tablename__ = "users"

    username = db.Column(
        db.String(20),
        primary_key = True,
    )

    password = db.Column(
        db.String(100),
        nullable = False
    )

    email = db.Column(
        db.String(50),
        nullable = False
    )
    first_name = db.Column(
        db.String(30),
        nullable = False
    )
    last_name = db.Column(
        db.String(30),
        nullable = False
    )

    def __repr__(self):
        return f"User: {self.username} email: {self.email}"


def connect_db(app):
    """Connect to database."""

    app.app_context().push()
    db.app = app
    db.init_app(app)