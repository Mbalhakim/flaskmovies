from flask import Flask, flash, g, render_template, request, redirect, url_for, session, jsonify
import os
import sqlite3


app = Flask(__name__)
app.secret_key = os.urandom(24)

def create_users_table():
    conn = sqlite3.connect('users.db')
    c = conn.cursor()
    c.execute('''CREATE TABLE IF NOT EXISTS users
                 (username TEXT PRIMARY KEY, password TEXT)''')
    conn.commit()
    conn.close()

# insert new user into database
def insert_user(username, password):
    conn = sqlite3.connect('users.db')
    c = conn.cursor()
    c.execute('INSERT INTO users VALUES (?, ?)', (username, password))
    conn.commit()
    conn.close()

# check if user exists in database
def user_exists(username):
    conn = sqlite3.connect('users.db')
    c = conn.cursor()
    c.execute('SELECT * FROM users WHERE username=?', (username,))
    result = c.fetchone()
    conn.close()
    return result is not None

# get password for user from database
def get_password(username):
    conn = sqlite3.connect('users.db')
    c = conn.cursor()
    c.execute('SELECT password FROM users WHERE username=?', (username,))
    result = c.fetchone()
    conn.close()
    return result[0] if result is not None else None

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        if user_exists(username) and get_password(username) == password:
            session['username'] = username
            return redirect(url_for('index'))
        else:
            return render_template('login.html', error='Invalid username or password')
    return render_template('login.html')

# registration route
@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        if user_exists(username):
            return render_template('register.html', error='Username already exists')
        else:
            insert_user(username, password)
            return redirect(url_for('login'))
    return render_template('register.html')




@app.route('/logout')
def logout():
    session.pop('username', None)
    return redirect(url_for('index'))

if __name__ == '__main__':
    create_users_table()
    app.run(debug=True)

JOBS= [
    {'id' : 1,
     'title': 'AI Engineer',
     'location': 'Netherlands, Rotterdam',
     'salaris': 3500
     },
{'id' : 4,
     'title': 'Front-end Developer',
     'location': 'Netherlands, Arnhem',
     'salaris': 2900
     },

{'id' : 1,
     'title': 'Data Analist',
     'location': 'Netherlands, Amsterdam',
     'salaris': 4500
     },
{'id' : 1,
     'title': 'App Developer',
     'location': 'Netherlands, Utrecht',
     'salaris': 3200
     }
]
@app.route("/")
def hello_world():
    return render_template('home.html',
                           jobs=JOBS)
@app.route("/api/jobs")
def list_jobs():
    return jsonify(JOBS)

@app.route('/users/create', methods=['GET', 'POST'])
def create_user():
    if request.method == 'POST':
        conn = sqlite3.connect('moviefan.db')
        c = conn.cursor()
        c.execute('INSERT INTO user (id, email, username, password) VALUES (?, ?)',
                  (request.form['title'], request.form['year']))
        conn.commit()
        conn.close()
        return redirect('/movies')
    else:
        return render_template('create_movie.html')

if __name__ == "__main__":
    app.run(host='0.0.0.0', debug=True)