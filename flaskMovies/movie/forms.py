from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SelectField, SubmitField, DateField, TextAreaField
from wtforms.validators import DataRequired, EqualTo, Email
from wtforms import ValidationError
from flaskMovies.models import User, Movie
from flask import request

class Update_description(FlaskForm):
    description = TextAreaField("Beschrijving:", validators=[DataRequired()])
    submit = SubmitField('Opslaan')

class Add_quote(FlaskForm):
    quote = TextAreaField("Citaat toevoegen:", validators=[DataRequired()])
    submit = SubmitField('Toevoegen')