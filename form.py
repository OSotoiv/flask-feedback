from flask_wtf import FlaskForm
from wtforms import StringField, IntegerField, BooleanField, RadioField, SelectField, URLField, EmailField, PasswordField, TextAreaField
from wtforms.validators import InputRequired, Optional, NumberRange, ValidationError


class User_Form(FlaskForm):

    username = StringField('User Name', validators=[InputRequired()])
    email = EmailField('Email', validators=[InputRequired()])
    password = PasswordField('Password', validators=[InputRequired()])
    first_name = StringField('First Name', validators=[InputRequired()])
    last_name = StringField('Last Name', validators=[InputRequired()])


class Login_Form(FlaskForm):
    username = StringField('User Name', validators=[InputRequired()])
    password = PasswordField('Password', validators=[InputRequired()])


class Feedback_Form(FlaskForm):
    title = StringField('Title', validators=[InputRequired()])
    content = TextAreaField('Feedback', validators=[InputRequired()])
