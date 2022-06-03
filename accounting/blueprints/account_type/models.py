from accounting import db
from .. data_model import DataModel


class AccountType(db.Model, DataModel):
    __tablename__ = "tbl_account_type"

    account_type = db.Column(db.String(64), unique=True, nullable=False)
    classification = db.Column(db.String(8), nullable=False)
    priority = db.Column(db.String(8), nullable=False)

    user_id = db.Column(db.Integer, db.ForeignKey('tbl_user.id'), nullable=False)
    user = db.relationship('User', backref=db.backref(__tablename__, lazy=True))

    def __repr__(self):
        return self.account_type

    @staticmethod
    def classification_choices():
        return ["", "Real", "Nominal"]


