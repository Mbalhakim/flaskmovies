from flask import Flask, render_template
from flaskMovies.models import Movie
from flaskMovies import app
import random


### ROUTES:

@app.route('/')
def index():
     allmovies = Movie.query.all()
     movies = random.sample(allmovies, 8)
     return render_template('index.html', movies=movies)

@app.route('/films')
def films():
     movies = Movie.query.all()
     return render_template('films.html', movies=movies)

@app.route('/about')
def about():
     return render_template('about.html')



# Register login function to the /user route


if __name__ == "__main__":
    app.run(debug=True)