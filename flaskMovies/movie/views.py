from flaskMovies import db
from flask import Blueprint, render_template, redirect, request, url_for, flash, session
from flask_login import login_user, login_required, logout_user, current_user
from flaskMovies.models import User, Category, Movie, Director, Actor, Movie_actor, Role, Quote
from flaskMovies.movie.forms import Update_description, Add_quote
from functools import wraps
from datetime import datetime, time
from sqlalchemy import desc

movie_blueprint = Blueprint('movie', __name__, template_folder='templates')

@movie_blueprint.route('/<string:name>/<int:id>', methods=['GET', 'POST'])
def movie_page(name, id):
    form1 = Update_description()
    form2 = Add_quote()
    movie = Movie.query.filter_by(id=id).first()
    category = Category.query.filter_by(id=movie.category_id).first()
    movie_actor = Actor.query.join(Movie_actor).filter(Movie_actor.movie_id==id) \
        .order_by(Actor.firstname).all()
    actors = [[actor.firstname, actor.lastname, actor.id] for actor in movie_actor]
    director = Director.query.filter_by(id=movie.director_id).first()
    role_list = []
    for i in actors:
        actor_role = Role.query.join(Actor).filter(Actor.id==i[2]) \
            .order_by(Actor.firstname).first()
        role_list.append(actor_role)
        
    roles = [role.name for role in role_list]
    for i in range(len(actors)):
        actors[i].append(roles[i])
        
    quotes_user = Quote.query.join(Movie).filter(Movie.id==id) \
            .order_by(desc(Quote.id), desc(Quote.date), desc(Quote.time)).all()
    quotes = [[q.quote, q.date, q.time, q.user_id] for q in quotes_user]
    user_list = []
    print(quotes)
    for i in quotes:
        user = User.query.join(Quote).filter(Quote.user_id==i[3]) \
            .first()
        user_list.append(user)
        
    users = [user.username for user in user_list]
   
    for i in range(len(quotes)):
        quotes[i].append(users[i])
    print(quotes)
    
    return render_template('movie.html', movie=movie, category=category, actors=actors,
                           director=director, form1=form1, form2=form2, quotes=quotes)

@movie_blueprint.route('/update_desc/<int:id>', methods=['GET', 'POST'])
@login_required
def update_description(id):
    form1 = Update_description()
    movie = Movie.query.filter_by(id=id).first()
    
    if form1.validate_on_submit():
        movie.description = form1.description.data
        db.session.commit()
        flash('De Beschrijving is bijgewerkt!')
    return redirect(url_for('movie.movie_page', name=movie.title.replace(' ', '-'), id=movie.id))

@movie_blueprint.route('/add_quote/<int:id>', methods=['GET', 'POST'])
@login_required
def add_quote(id):
    form2 = Add_quote()
    movie = Movie.query.filter_by(id=id).first()

    if form2.validate_on_submit():
        user_id = session['user_id']
        current_date = datetime.now().date()
        now = datetime.now().time()
        current_time = time(now.hour, now.minute)
        print(current_time)
        # add to db
        quote = Quote(quote=form2.quote.data,
                    date=current_date,
                    time=current_time,
                    movie_id=movie.id, 
                    user_id=user_id)
        db.session.add(quote)
        db.session.commit()
        flash('De citaat is toegevoegd!')
    return redirect(url_for('movie.movie_page', name=movie.title.replace(' ', '-'), id=movie.id))

