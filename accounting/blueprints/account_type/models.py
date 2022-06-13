from accounting import db
from .. data_model import DataModel


class AccountType(db.Model, DataModel):
    account_type = db.Column(db.String(64), unique=True, nullable=False)
    classification = db.Column(db.String(8), nullable=False)
    priority = db.Column(db.String(8), nullable=False)

    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    date_modified = db.Column(db.DateTime, nullable=True)

    def __repr__(self):
        return self.account_type

    @staticmethod
    def classification_choices():
        return ["", "Real", "Nominal"]


