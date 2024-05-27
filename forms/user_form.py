from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, EmailField
from wtforms.validators import InputRequired, DataRequired, Email, Length

class RegisterForm(FlaskForm):
    first_name = StringField('First Name', validators=[DataRequired()])
    last_name = StringField('Last Name', validators=[DataRequired()])
    username = StringField('Username', validators=[DataRequired(), Length(min=5, max=25)])
    email = EmailField('Email', validators=[InputRequired(), Email()])
    password = PasswordField('Password', validators=[InputRequired(), Length(min=8, max=20)])
    confirm_password = PasswordField('Confirm Password', validators=[InputRequired(), Length(min=8, max=20)])

class LoginForm(FlaskForm):
    username = StringField('Username', validators=[InputRequired(), Length(min=5, max=25)])
    password = PasswordField('Password', validators=[InputRequired(), Length(min=8, max=20)])