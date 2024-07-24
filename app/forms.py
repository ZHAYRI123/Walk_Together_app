from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, TextAreaField, BooleanField
from wtforms.validators import DataRequired, Length, Email, EqualTo
from email_validator import validate_email

class RegistrationForm(FlaskForm):
    email = StringField('Email', validators=[DataRequired(), Email()])
    name = StringField('Name', validators=[DataRequired(), Length(min=1, max=150)])
    password = PasswordField('Password', validators=[DataRequired(), Length(min=8)])
    confirm_password = PasswordField('Confirm Password', validators=[DataRequired(), EqualTo('password')])
    submit = SubmitField('Sign Up')

class LoginForm(FlaskForm):
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    remember_me = BooleanField('Remember Me') # type: ignore
    submit = SubmitField('Login')

class TaskForm(FlaskForm):
    description = TextAreaField('Task Description', validators=[DataRequired()])
    submit = SubmitField('Complete Task')

class ChallengeForm(FlaskForm):
    title = StringField('Title', validators=[DataRequired(), Length(min=1, max=150)])
    description = TextAreaField('Description', validators=[DataRequired()])
    submit = SubmitField('Create Challenge')
