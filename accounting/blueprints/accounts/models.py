from accounting import db
from .. data_model import DataModel


class Accounts(db.Model, DataModel):
    account_number = db.Column(db.String(32), nullable=False)
    account_title = db.Column(db.String(255), nullable=False)
    account_type_id = db.Column(db.Integer, db.ForeignKey('account_type.id'), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    date_modified = db.Column(db.DateTime, nullable=True)

    def __repr__(self):
        return f"{self.account_number}: {self.account_title}"
