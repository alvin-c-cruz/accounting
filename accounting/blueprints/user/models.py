from accounting import db
from flask_login import UserMixin


class User(UserMixin, db.Model):
    id = db.Column(db.Integer(), primary_key=True)
    email = db.Column(db.String(), unique=True, nullable=False)
    password = db.Column(db.String(), nullable=False)
    name = db.Column(db.String(), nullable=True)
    admin = db.Column(db.Boolean(), default=False)
    registered_on = db.Column(db.DateTime, nullable=True)
    confirmed_on = db.Column(db.DateTime, nullable=True)


