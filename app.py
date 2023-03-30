from flask import Flask, render_template, flash, redirect, url_for, session
from forms import AddFilmForm, Login

app = Flask(__name__)
app.config['SECRET_KEY'] = "yusegfugwsefv43543yu"


### ROUTES:

@app.route('/')
def index():

     return render_template('index.html')

# @app.route('/addfilm', methods=['post'])
@app.route('/addfilm')
def addfilm():
     addForm = AddFilmForm()
#     form.category.choices = [(cat.id, cat.name) for cat in Category.query.order_by('name')]

     return render_template('addfilm.html', form=addForm)

# @app.route('/login', methods=['post'])
@app.route('/login')
def login():
     loginForm = Login()
     return render_template('login.html', form=loginForm)

if __name__ == "__main__":
    app.run(debug=True)