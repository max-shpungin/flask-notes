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

    @classmethod
    def register(cls, username, password, email, first_name, last_name):
        """Registers new user with a properly hashed password and return that
        new user"""

        hash_pwd = bcrypt.generate_password_hash(password).decode('utf8')

        return cls(
            username=username,
            password=hash_pwd,
            email=email,
            first_name=first_name,
            last_name=last_name)

    @classmethod
    def authenticate(cls, username, password):
        """ Validate user exists and password is correct
            Return user instance if valid, else False
        """

        user = cls.query.filter_by(username=username).one_or_none()

        if user and bcrypt.check_password_hash(user.password, password):
            return user
        else:
            return None #FIXME: ? returning False feels weird vs demo code?

def connect_db(app):
    """Connect to database."""

    app.app_context().push()
    db.app = app
    db.init_app(app)