from flask_wtf import FlaskForm
from wtforms import StringField, TextAreaField, SelectField, EmailField
from wtforms.validators import InputRequired, DataRequired, Email

class TicketForm(FlaskForm):
    subject = StringField('Subject', validators=[DataRequired()])
    description = TextAreaField('Description', validators=[DataRequired()])
    priority = SelectField('Priority', choices=[('', 'Choose an option'), ('Low', 'Low'), ('Medium', 'Medium'), ('High', 'High')], validators=[DataRequired(message='Please select a priority')])
    email = EmailField('Email', validators=[InputRequired(), Email()])