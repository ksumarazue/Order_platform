from infra.database import db


class User(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    name = db.Column(db.String(20), unique = True, nullable = False)
    email = db.Column(db.String(50), unique = True, nullable = False)
    password = db.Column(db.String(50), unique = False, nullable = False)
    group = db.Column(db.String(50), unique = False, nullable = False)