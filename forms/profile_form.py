from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, EmailField, SelectField
from wtforms.validators import InputRequired, DataRequired, Email, Length, EqualTo

class ProfileForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired(), Length(min=5, max=25)])
    email = EmailField('Email', validators=[InputRequired(), Email()])
    role = SelectField('Role', choices=[('Admin', 'Admin'), ('Standard User', 'Standard User')], validators=[DataRequired()])
