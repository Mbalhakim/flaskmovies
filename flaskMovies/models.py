from flaskMovies import db, login_manager
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import UserMixin
from datetime import datetime

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(user_id)

class User(db.Model, UserMixin):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key = True)
    firstname = db.Column(db.String(64))
    lastname = db.Column(db.String(64))
    email = db.Column(db.String(64), unique=True, index=True)
    username = db.Column(db.String(64), unique=True, index=True)
    is_admin = db.Column(db.Boolean, default=False)
    password_hash = db.Column(db.String(128))

    def __init__(self, firstname, lastname, email, username, password):
        self.firstname = firstname
        self.lastname = lastname
        self.email = email
        self.username = username
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

class Category(db.Model):
    __tablename__ = 'category'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.Text, nullable=False)

    def __init__(self, name):
        self.name = name
        
class Director(db.Model):
    __tablename__ = 'director'
    id = db.Column(db.Integer, primary_key=True)
    firstname = db.Column(db.String(64), nullable=False)
    lastname = db.Column(db.String(64), nullable=False)

    def __init__(self, firstname, lastname):
        self.firstname = firstname
        self.lastname = lastname
        
class Actor(db.Model):
    __tablename__ = 'actor'
    id = db.Column(db.Integer, primary_key=True)
    firstname = db.Column(db.String(64), nullable=False)
    lastname = db.Column(db.String(64), nullable=False)

    def __init__(self, firstname, lastname):
        self.firstname = firstname
        self.lastname = lastname

class Movie(db.Model):
    __tablename__ = 'movies'
    id = db.Column(db.Integer, primary_key = True)
    title = db.Column(db.Text, nullable=False)
    description = db.Column(db.Text)
    release_date = db.Column(db.Date)
    image = db.Column(db.Text)
    trailer = db.Column(db.Text)
    
    category_id = db.Column(db.Integer, db.ForeignKey('category.id'))
    category = db.relationship('Category', backref='Movie', uselist=False)
    
    director_id = db.Column(db.Integer, db.ForeignKey('director.id'))
    director = db.relationship('Director', backref='Movie', uselist=False)

    def __init__(self, title, description, release_date, image, trailer, category_id, director_id):
        self.title = title
        self.description = description
        self.release_date = release_date
        self.image = image
        self.trailer = trailer
        self.category_id = category_id
        self.director_id = director_id
        
class Movie_actor(db.Model):
    __tablename__ = 'movie_actor'
    id = db.Column(db.Integer, primary_key=True)
    movie_id = db.Column(db.Integer, db.ForeignKey('movies.id'))
    movie = db.relationship('Movie', backref='Movie_actor', uselist=False)
    
    actor_id = db.Column(db.Integer, db.ForeignKey('actor.id'))
    actor = db.relationship('Actor', backref='Movie_actor', uselist=False)

    def __init__(self, movie_id, actor_id):
        self.movie_id = movie_id
        self.actor_id = actor_id
        
class Role(db.Model):
    __tablename__ = 'role'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.Text)
    
    movie_id = db.Column(db.Integer, db.ForeignKey('movies.id'))
    movie = db.relationship('Movie', backref='Role', uselist=False)
    
    actor_id = db.Column(db.Integer, db.ForeignKey('actor.id'))
    actor = db.relationship('Actor', backref='Role', uselist=False)

    def __init__(self, name, movie_id, actor_id):
        self.name = name
        self.movie_id = movie_id
        self.actor_id = actor_id
        
class Quote(db.Model):
    __tablename__ = 'quotes'
    id = db.Column(db.Integer, primary_key=True)
    quote = db.Column(db.Text)
    date = db.Column(db.Date)
    time = db.Column(db.Time)

    movie_id = db.Column(db.Integer, db.ForeignKey('movies.id'))
    movie = db.relationship('Movie', backref='Quote', uselist=False)
    
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    user = db.relationship('User', backref='Quote', uselist=False)

    def __init__(self, quote, date, time, movie_id, user_id):
        self.quote = quote
        self.date = date
        self.time = time
        self.movie_id = movie_id
        self.user_id = user_id
