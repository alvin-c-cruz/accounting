from flask_login import UserMixin
from accounting import db
from datetime import datetime
from .. data_model import DataModel


class User(UserMixin, db.Model, DataModel):
    email = db.Column(db.String(64), unique=True, nullable=False)
    password = db.Column(db.String(64), nullable=False)
    name = db.Column(db.String(64))
    admin = db.Column(db.Boolean(), default=False)
    registered_on = db.Column(db.DateTime, default=datetime.utcnow)
    confirmed_on = db.Column(db.DateTime)

    account_types = db.relationship('AccountType', backref="user", lazy="joined")
    vendors = db.relationship('Vendors', backref="user", lazy="joined")

    def __repr__(self):
        return self.name
