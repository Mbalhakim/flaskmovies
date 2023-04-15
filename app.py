from flask import Flask, render_template
from flaskMovies.models import Movie
from flaskMovies import app

### ROUTES:

@app.route('/')
def index():
     movies = Movie.query.all()
     return render_template('index.html', movies=movies)

@app.route('/films')
def films():
     movies = Movie.query.all()
     return render_template('films.html', movies=movies)

@app.route('/about')
def about():
     return render_template('about.html')

if __name__ == "__main__":
    app.run(debug=True)