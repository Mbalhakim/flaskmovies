from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SelectField, SubmitField, DateField, TextAreaField
from wtforms.validators import DataRequired, EqualTo, Email
from wtforms import ValidationError
from flaskMovies.models import User, Movie

class RegistrationForm(FlaskForm):
    firstname = StringField('Voornaam', validators=[DataRequired()])
    lastname = StringField('Achternaam', validators=[DataRequired()])
    username = StringField('Gebruikersnaam', validators=[DataRequired()])
    email = StringField("E-mail:", validators=[Email()])
    password = PasswordField('Wachtwoord', validators=[DataRequired(), EqualTo('pass_confirm', message='Wachtwoorden dienen overeen te komen')])
    pass_confirm = PasswordField('Bevestig wachtwoord', validators=[DataRequired()])
    submit = SubmitField('Registreer')
        
    def validate_username(self, field):
        no_space = field.data.replace(" ", "")
        if User.query.filter_by(username=field.data).first() or Movie.query.filter_by(username=no_space).first():
            raise ValidationError('Deze gebruikersnaam is al vergeven, probeer een andere naam')
        
    def validate_email(self, field):
        no_space = field.data.replace(" ", "")
        if User.query.filter_by(email=field.data).first() or Movie.query.filter_by(email=no_space).first():
            raise ValidationError('Deze emailadres is al in gebruik')

class LoginForm(FlaskForm):
    username = StringField('Gebruikersnaam', validators=[DataRequired()])
    password = PasswordField('Wachtwoord', validators=[DataRequired()])
    submit = SubmitField('Inloggen')
    
class AddFilmForm(FlaskForm):
    title = StringField("Titel:", validators=[DataRequired()])
    description = TextAreaField("Beschrijving:", validators=[DataRequired()])
    release_date = DateField('Release datum:', format='%Y-%m-%d', validators=[DataRequired()])
    category = SelectField('Categorie:', choices=[])
    director_firstname = StringField("Voornaam:", validators=[DataRequired()])
    director_lastname = StringField("Achternaam:", validators=[DataRequired()])
    actor1_firstname = StringField("Voornaam:", validators=[DataRequired()])
    actor1_lastname = StringField("Achternaam:", validators=[DataRequired()])
    actor2_firstname = StringField("Voornaam:", validators=[DataRequired()])
    actor2_lastname = StringField("Achternaam:", validators=[DataRequired()])
    actor3_firstname = StringField("Voornaam:", validators=[DataRequired()])
    actor3_lastname = StringField("Achternaam:", validators=[DataRequired()])
    actor4_firstname = StringField("Voornaam:", validators=[DataRequired()])
    actor4_lastname = StringField("Achternaam:", validators=[DataRequired()])
    submit = SubmitField("Toevoegen")
    
    
    def validate_title(self, field):
        no_space = field.data.replace(" ", "")
        if Movie.query.filter_by(title=field.data).first() or Movie.query.filter_by(title=no_space).first():
            raise ValidationError('Deze film bestaat al')