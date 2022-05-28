from accounting import db
from .. data_model import DataModel


class AccountType(db.Model, DataModel):
    __tablename__ = "tbl_account_type"

    account_type = db.Column(db.String(64), unique=True, nullable=False)
    classification = db.Column(db.String(8), nullable=False)
    prefix = db.Column(db.String(8), nullable=False)

    def __repr__(self):
        return self.account_type

    def choices(self):
        data = db.query(self).order_by(self.priority).all()
        data.insert(0, "")
        return data

    @staticmethod
    def classification_choices():
        return ["", "Real", "Nominal"]


