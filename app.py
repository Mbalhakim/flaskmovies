from flask import Flask, render_template
from flaskMovies import app

### ROUTES:

@app.route('/')
def index():
     return render_template('index.html')

if __name__ == "__main__":
    app.run(debug=True)