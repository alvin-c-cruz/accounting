from accounting import db
from .. data_model import DataModel


class Accounts(db.Model, DataModel):
    __tablename__ = "tbl_accounts"

    account_number = db.Column(db.String(32), nullable=False)
    account_title = db.Column(db.String(255), nullable=False)

    account_type_id = db.Column(db.Integer, db.ForeignKey('tbl_account_type.id'), nullable=False)
    account_type = db.relationship('AccountType', backref=db.backref('tbl_accounts', lazy=True))

    def __repr__(self):
        return f"{self.account_number}: {self.account_title}"
