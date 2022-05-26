from flask_login import UserMixin
from accounting import db
from .. data_model import DataModel


class User(UserMixin, db.Model, DataModel):
    __tablename__ = "tbl_user"

    email = db.Column(db.String(64), unique=True, nullable=False)
    password = db.Column(db.String(64), nullable=False)
    name = db.Column(db.String(64))
    admin = db.Column(db.Boolean(), default=False)
    registered_on = db.Column(db.DateTime)
    confirmed_on = db.Column(db.DateTime)
