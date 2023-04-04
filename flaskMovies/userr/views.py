from flaskMovies import db
from flask import Blueprint, render_template, redirect, request, url_for, flash, session
from flask_login import login_user, login_required, logout_user, current_user
from flaskMovies.models import User
from flaskMovies.userr.forms import LoginForm, RegistrationForm, AddFilmForm
from functools import wraps

userr_blueprint = Blueprint('userr', __name__, template_folder='templates')

@userr_blueprint.route('/logout')
@login_required
def logout():
    logout_user()
    session.clear()
    flash('U bent nu uitgelogd')
    return redirect(url_for('index'))

def admin_required(func):
    @wraps(func)
    def decorated_view(*args, **kwargs):
        if not current_user.is_admin:
            return redirect('/')
        return func(*args, **kwargs)
    return decorated_view

@userr_blueprint.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        if user is not None and user.check_password(form.password.data):
            login_user(user)
            session['username'] = user.username
            session['firstname'] = user.firstname
            session['lastname'] = user.lastname
            if user.is_admin:
                return redirect(url_for('userr.dashboard'))
            else:
                flash('U bent succesvol ingelogd')
                return redirect('/')
        # else:
        #     return render_template('login.html', error='Invalid username or password')
    return render_template('login.html', form=form)

@userr_blueprint.route('/register', methods=['GET', 'POST'])
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
        return redirect(url_for('userr.login'))
    return render_template('register.html', form=form)


@userr_blueprint.route('/dashboard')
@login_required
@admin_required
def dashboard():
    all_users = User.query.all()
    return render_template('admin_dashboard.html', users=all_users)

@userr_blueprint.route('/addfilm')
@login_required
@admin_required
def addfilm():
    addForm = AddFilmForm()
    return render_template('addfilm.html', form=addForm)
    
@userr_blueprint.route('/film_manager')
@login_required
@admin_required
def film_manager():
    addForm = AddFilmForm()
    return render_template('film_manager.html', form=addForm)
    
    