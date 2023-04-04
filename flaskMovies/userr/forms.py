from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SelectField, SubmitField, DateField, TextAreaField
from wtforms.validators import DataRequired, EqualTo, Email
from wtforms import ValidationError
from flaskMovies.models import User

class RegistrationForm(FlaskForm):
    firstname = StringField('Voornaam', validators=[DataRequired()])
    lastname = StringField('Achternaam', validators=[DataRequired()])
    username = StringField('Gebruikersnaam', validators=[DataRequired()])
    email = StringField("E-mail:", validators=[Email()])
    password = PasswordField('Wachtwoord', validators=[DataRequired(), EqualTo('pass_confirm', message='Wachtwoorden dienen overeen te komen')])
    pass_confirm = PasswordField('Bevestig wachtwoord', validators=[DataRequired()])
    submit = SubmitField('Registreer')
        
    def validate_username(self, field):
        if User.query.filter_by(username=field.data).first():
            raise ValidationError('Deze gebruikersnaam is al vergeven, probeer een andere naam')

class LoginForm(FlaskForm):
    username = StringField('Gebruikersnaam', validators=[DataRequired()])
    password = PasswordField('Wachtwoord', validators=[DataRequired()])
    submit = SubmitField('Inloggen')
    
class AddFilmForm(FlaskForm):
    title = StringField("Titel:")
    description = TextAreaField("Beschrijving:")
    release_date = DateField('Release datum:', format='%Y-%m-%d')
    # category = SelectField('Categorie:', choices=[])
    category = SelectField('Categorie:')
    director_firstname = StringField("Voornaam:")
    director_lastname = StringField("Achternaam:")
    actor1_firstname = StringField("Voornaam:")
    actor1_lastname = StringField("Achternaam:")
    actor2_firstname = StringField("Voornaam:")
    actor2_lastname = StringField("Achternaam:")
    actor3_firstname = StringField("Voornaam:")
    actor3_lastname = StringField("Achternaam:")
    actor4_firstname = StringField("Voornaam:")
    actor4_lastname = StringField("Achternaam:")
    submit = SubmitField("Toevoegen")