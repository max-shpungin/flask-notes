from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, TextAreaField
from wtforms.validators import InputRequired, Email, Length

class RegisterForm(FlaskForm):

    username = StringField("Enter a username: ",
                           validators=[InputRequired(), Length(min=1, max=20)])

    password = PasswordField("Enter a password: ",
                           validators=[InputRequired(), Length(min=1, max=100)])

    email = StringField("Enter a email: ",
                           validators=[InputRequired(), Email(),
                                        Length(min=1, max=50)])

    first_name = StringField("Enter a first name: ",
                           validators=[InputRequired(), Length(min=1, max=30)])

    last_name = StringField("Enter a last name: ",
                           validators=[InputRequired(), Length(min=1, max=30)])

class LoginForm(FlaskForm):
     username = StringField("Enter a username: ",
                           validators=[InputRequired(), Length(min=1, max=20)])
     password = PasswordField("Enter a password: ",
                            validators=[InputRequired(), Length(min=1, max=100)])

class AddNoteForm(FlaskForm):
     title = StringField("Enter a title: ",
                           validators=[InputRequired(), Length(min=1, max=100)])
     content = TextAreaField("Enter content: ",
                            validators=[InputRequired()])

class CSRFProtectForm(FlaskForm):
     """Form for CSRF Protection"""