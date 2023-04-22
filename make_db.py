from flaskMovies import db, app
from flaskMovies.models import Category

with app.app_context():
    db.create_all()
    # db.session.add_all([Category('Mystery')])
    db.session.commit()