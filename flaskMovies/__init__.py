from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
import os


basedir = os.path.abspath(os.path.dirname(__file__))

app = Flask(__name__)
app.config['SECRET_KEY'] = "dhjdjhgdhgdghdghdjhgdjhdjh"
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(basedir, 'moviefan.sqlite')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = "user.login"

from flaskMovies.user.views import user_blueprint
app.register_blueprint(user_blueprint, url_prefix="/user")

from flaskMovies.movie.views import movie_blueprint
app.register_blueprint(movie_blueprint, url_prefix="/movie")