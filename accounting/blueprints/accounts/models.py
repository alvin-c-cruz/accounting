from accounting import db
from .. data_model import DataModel


class Accounts(db.Model, DataModel):
    id = db.Column(db.Integer, primary_key=True)
    account_number = db.Column(db.String(32), nullable=False, unique=True)
    account_title = db.Column(db.String(255), nullable=False, unique=True)

    account_type_id = db.Column(db.Integer, db.ForeignKey('account_type.id'), nullable=False)
    account_type = db.relationship('AccountType', backref="accounts")

    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    user = db.relationship('User', backref="accounts")

    date_modified = db.Column(db.DateTime, nullable=True)

    def __repr__(self):
        return f"{self.account_number}: {self.account_title}"


def account_choices():
    data = [(row.id, row) for row in Accounts.query.order_by(Accounts.account_number).all()]
    data.insert(0, ("", ""))
    return data