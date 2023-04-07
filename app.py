from flask import Flask, render_template
from flaskMovies.models import Movie
from flaskMovies import app

### ROUTES:

@app.route('/')
def index():
     movies = Movie.query.all()
     return render_template('index.html', movies=movies)

if __name__ == "__main__":
    app.run(debug=True)