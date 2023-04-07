from flaskMovies import db
from flask import Blueprint, render_template, redirect, request, url_for, flash, session
from flask_login import login_user, login_required, logout_user, current_user
from flaskMovies.models import User, Category, Movie, Director, Actor, Movie_actor
from flaskMovies.userr.forms import LoginForm, RegistrationForm, AddFilmForm
from functools import wraps

movie_blueprint = Blueprint('movie', __name__, template_folder='templates')

@movie_blueprint.route('/<string:name>/<int:id>', methods=['GET', 'POST'])
def movie_page(name, id):
    movie = Movie.query.filter_by(id=id).first()
    return render_template('movie.html', movie=movie)