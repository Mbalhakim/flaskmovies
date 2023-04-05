from flaskMovies import db, app
from flaskMovies.models import Category

with app.app_context():
    db.create_all()
    db.session.add_all([Category('Cat_1'), Category('Cat_2'), Category('Cat_3'), Category('Cat_4')])
    db.session.commit()