from flask_wtf import FlaskForm
from wtforms import StringField, SelectField, SubmitField, DateField, TextAreaField, PasswordField
from wtforms.validators import Email


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


class Login(FlaskForm):
    email = StringField("E-mail:", validators=[Email()], render_kw={"placeholder": "E-mail"})
    password = PasswordField("Wachtwoord:", render_kw={"placeholder": "Wachtwoord"})
    submit = SubmitField("Inloggen")