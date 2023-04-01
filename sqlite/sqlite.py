import sqlite3

conn = sqlite3.connect('moviefan.db')
c = conn.cursor()

# create the movie table
c.execute(''' CREATE TABLE IF NOT EXISTS movie 
             (id INTEGER PRIMARY KEY, title TEXT NOT NULL, description TEXT , release_date DATE, category_id INTEGER, FOREIGN KEY (category_id) REFERENCES category(id))''')

# create the movie_actor table
c.execute('''CREATE TABLE IF NOT EXISTS movie_actor
             (id INTEGER PRIMARY KEY, movie_id INTEGER, actor_id INTEGER, FOREIGN KEY (movie_id) REFERENCES movie(id), FOREIGN KEY (actor_id) REFERENCES actor(id))''')

# create the actor table
c.execute('''CREATE TABLE IF NOT EXISTS actor
             (id INTEGER PRIMARY KEY, firstname TEXT NOT NULL, lastname TEXT NOT NULL, image TEXT NOT NULL )''')

# create the director table
c.execute('''CREATE TABLE IF NOT EXISTS director
             (id INTEGER PRIMARY KEY, firstname TEXT NOT NULL, lastname TEXT NOT NULL, image TEXT NOT NULL)''')

# create the movie_director table
c.execute('''CREATE TABLE IF NOT EXISTS movie_director
             (id INTEGER PRIMARY KEY, movie_id INTEGER, director_id INTEGER, FOREIGN KEY (movie_id) REFERENCES movie(id), FOREIGN KEY (director_id) REFERENCES director(id))''')

# create the category table
c.execute('''CREATE TABLE IF NOT EXISTS category
             (id INTEGER PRIMARY KEY, name TEXT NOT NULL)''')

# create the user table
c.execute('''CREATE TABLE IF NOT EXISTS user
             (id INTEGER PRIMARY KEY, email TEXT NOT NULL, username TEXT NOT NULL, password TEXT NOT NULL)''')

# commit the changes and close the connection
conn.commit()
conn.close()
