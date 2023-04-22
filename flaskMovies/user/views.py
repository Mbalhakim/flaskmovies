from flaskMovies import db
from flask import Blueprint, render_template, redirect, request, url_for, flash, session
from flask_login import login_user, login_required, logout_user, current_user
from flaskMovies.models import User, Category, Movie, Director, Actor, Movie_actor, Role, Quote
from flaskMovies.user.forms import LoginForm, RegistrationForm, AddFilmForm, UpdateUserForm
from functools import wraps

user_blueprint = Blueprint('user', __name__, template_folder='templates')







@user_blueprint.route('/logout')
@login_required
def logout():
    logout_user()
    session.clear()
    return redirect(url_for('index'))

def admin_required(func):
    @wraps(func)
    def decorated_view(*args, **kwargs):
        if not current_user.is_admin:
            return redirect('/')
        return func(*args, **kwargs)
    return decorated_view

@user_blueprint.route('/dashboard')
@admin_required
def dashboard():
    movies = Movie.query.all()
    users = User.query.all()
    return render_template('admin_dashboard.html', users=users, movies=movies)

@user_blueprint.route('/users/update/<int:user_id>', methods=['GET', 'POST'])
@login_required
@admin_required
def update_user(user_id):
    user = User.query.get(user_id)
    form = UpdateUserForm(obj=user)
    if form.validate_on_submit():
        form.populate_obj(user)
        db.session.commit()
        flash('User updated successfully', 'success')
        return redirect(url_for('user.dashboard'))

    return render_template('update_user.html', form=form)

@user_blueprint.route('/<int:user_id>/delete', methods=['POST'])
@admin_required
@login_required
def delete_user(user_id):
    user = User.query.filter_by(id=user_id).first_or_404()
    db.session.delete(user)
    db.session.commit()
    flash('User has been deleted', 'success')
    return redirect(url_for('user.dashboard'))

@user_blueprint.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('user.dashboard'))
    
    form = LoginForm()
    error = None
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        if user is not None and user.check_password(form.password.data):
            login_user(user)
            session['user_id'] = user.id
            session['username'] = user.username
            session['firstname'] = user.firstname
            session['lastname'] = user.lastname
            if user.is_admin:
                return redirect(url_for('user.dashboard'))
            else:
                return redirect('/')
        else:
            error = 'De combinatie van gebruikersnaam en wachtwoord is niet geldig.'
    return render_template('login.html', form=form, error=error)

@user_blueprint.route('/register', methods=['GET', 'POST'])
def register():
    form = RegistrationForm()
    if form.validate_on_submit():
        # Add to db
        user = User(firstname=form.firstname.data,
                    lastname=form.lastname.data,
                    email=form.email.data,
                    username=form.username.data, 
                    password=form.password.data)
        db.session.add(user)
        db.session.commit()

        flash('Bedankt voor de registratie. Er kan nu ingelogd worden!')
        return redirect(url_for('user.login'))
    return render_template('register.html', form=form)

















@user_blueprint.route('/addfilm', methods=['GET', 'POST'])
@login_required
@admin_required
def addfilm():
    form = AddFilmForm()
    form.category.choices = [(cat.id, cat.name) for cat in Category.query.order_by('name')]
    director_exists = Director.query.filter_by(firstname=form.director_firstname.data, 
                                         lastname=form.director_lastname.data).first()
    director_id = None
    if form.validate_on_submit():
        # Add to db
        if director_exists is None:
            director = Director(form.director_firstname.data,
                                form.director_lastname.data)
            db.session.add(director)
            db.session.commit()
            director_id = director.id
        else:
            director_id = director_exists.id
            
        movie = Movie(title=form.title.data,
                    description=form.description.data,
                    release_date=form.release_date.data,
                    category_id=form.category.data,
                    image=form.image.data,
                    trailer=form.trailer.data,
                    director_id=director_id)
        db.session.add(movie)
        db.session.commit()
        for i in range(1, 5):
            actor_firstname = getattr(form, f'actor{i}_firstname').data
            actor_lastname = getattr(form, f'actor{i}_lastname').data
            actor_role = getattr(form, f'actor{i}_role').data
            actor_exists = Actor.query.filter_by(firstname=actor_firstname, lastname=actor_lastname).first()
            actor_id = None
            if actor_exists is None:
                actor = Actor(firstname=actor_firstname, lastname=actor_lastname)
                db.session.add(actor)
                db.session.commit()
                actor_id = actor.id
            else:
                actor_id = actor_exists.id

            movie_actor = Movie_actor(movie_id=movie.id, actor_id=actor_id)
            db.session.add(movie_actor)
            role = Role(movie_id=movie.id, actor_id=actor_id, name=actor_role)
            db.session.add(role)
            db.session.commit()
        
        flash(f"Film {form.title.data} is toegevoegd!")
        return redirect(url_for("user.addfilm"))
    return render_template('addfilm.html', form=form)
        
@user_blueprint.route('/film_manager')
@login_required
@admin_required
def film_manager():
    all_movies = Movie.query.all()
    return render_template('film_manager.html', movies=all_movies)

@user_blueprint.route('/delete/<int:id>', methods=['POST'])
@login_required
@admin_required
def delete_movie(id):
    movie_actors = Movie_actor.query.filter_by(movie_id=id).all()
    roles = Role.query.filter_by(movie_id=id).all()
    quotes = Quote.query.filter_by(movie_id=id).all()
    for movie_actor in movie_actors:
        db.session.delete(movie_actor)
    for role in roles:
        db.session.delete(role)
    for quote in quotes:
        db.session.delete(quote)
    movie = Movie.query.filter_by(id=id).first()
    db.session.delete(movie)
    db.session.commit()
    flash('De film is verwijderd!')
    return redirect(url_for('user.film_manager'))

@user_blueprint.route('/edit/<int:id>', methods=['GET', 'POST'])
@login_required
@admin_required
def edit_movie(id):
    form = AddFilmForm()
    movie = Movie.query.filter_by(id=id).first()
    form.category.choices = [(cat.id, cat.name) for cat in Category.query.order_by('name')]
    form.category.default = movie.category_id
    director = Director.query.filter_by(id=movie.director_id).first()
    movie_actor = Actor.query.join(Movie_actor).filter(Movie_actor.movie_id==id) \
        .order_by(Actor.firstname).all()
    actors = [[actor.firstname, actor.lastname, actor.id] for actor in movie_actor]

    role_list = []
    for i in actors:
        actor_role = Role.query.join(Actor).filter(Actor.id==i[2]) \
            .order_by(Actor.firstname).first()
        role_list.append(actor_role)
    
    roles = [role.name for role in role_list]
    for i in range(len(actors)):
        actors[i].append(roles[i])

    director_id = None
    if form.validate_on_submit():
        director_exists = Director.query.filter_by(firstname=form.director_firstname.data, 
                                         lastname=form.director_lastname.data).first()

        if director_exists is None:
            update_director = Director(form.director_firstname.data,
                                form.director_lastname.data)
            db.session.add(update_director)
            db.session.commit()
            director_id = update_director.id
        else:
            director_id = director_exists.id
        movie.title = form.title.data
        movie.description = form.description.data
        movie.release_date = form.release_date.data
        movie.image = form.image.data
        movie.trailer = form.trailer.data
        movie.director_id = director_id
        movie.category_id=form.category.data
        db.session.commit()
        
        ids = []
        roles_ = []
        movie_actor = Movie_actor.query.filter_by(movie_id=movie.id).all()
        current_actors = [ma.actor_id for ma in movie_actor]
            
        for i in range(1, 5):
            actor_firstname = f"{form['actor'+str(i)+'_firstname'].data}"
            actor_lastname = f"{form['actor'+str(i)+'_lastname'].data}"
            actor_role = f"{form['actor'+str(i)+'_role'].data}"
            actor_exists = Actor.query.filter_by(firstname=actor_firstname, lastname=actor_lastname).first()
 
            if actor_exists is None:
                actor = Actor(firstname=actor_firstname, lastname=actor_lastname)
                db.session.add(actor)
                db.session.commit()
                print('added: ', actor_firstname, actor_lastname, actor.id)
                ids.append(actor.id)
                roles_.append(actor_role)
            else:
                ids.append(actor_exists.id)
                roles_.append(actor_role)
        
        for actor_id in current_actors:
            if actor_id not in ids:
                Movie_actor.query.filter_by(movie_id=movie.id, actor_id=actor_id).delete()
                Role.query.filter_by(movie_id=movie.id, actor_id=actor_id).delete()
                db.session.commit()
                
        ids_roles = [[ids[i], roles_[i]] for i in range(len(ids))]
        
        for actor_id in ids:
            if actor_id not in current_actors:
                ma = Movie_actor(movie_id=movie.id, actor_id=actor_id)
                db.session.add(ma)
                for i in range(len(ids_roles)):
                    ar = Role(movie_id=movie.id, actor_id=ids_roles[i][0], name=ids_roles[i][1])
                    db.session.add(ar)
                    db.session.commit()
            else:
                print(ids_roles)
                for i in range(len(ids_roles)):
                    Role.query.filter_by(movie_id=movie.id, actor_id=ids_roles[i][0]).delete()
                    db.session.commit()
                    ar = Role(movie_id=movie.id, actor_id=ids_roles[i][0], name=ids_roles[i][1])
                    db.session.add(ar)
                    db.session.commit()
        
        flash('De film is bijgewerkt!')
        return redirect(url_for('user.film_manager'))
    return render_template('edit_movie.html', form=form, movie=movie, director=director, actors=actors, roles=roles)
    
    