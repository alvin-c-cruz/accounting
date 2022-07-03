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

    def balance(self):
        from .. sales import SalesEntry
        from .. receipts import ReceiptsEntry
        from .. accounts_payable import AccountsPayableEntry
        from .. disbursements import DisbursementsEntry
        from .. petty_cash import PettyCashEntry

        run_balance = 0
        for obj in (SalesEntry, ReceiptsEntry, AccountsPayableEntry, DisbursementsEntry, PettyCashEntry):
            for entry in obj.query.filter(obj.account_id == self.id).all():
                run_balance += entry.debit - entry.credit

        return run_balance


def account_choices():
    data = [(row.id, row) for row in Accounts.query.order_by(Accounts.account_number).all()]
    data.insert(0, ("", ""))
    return data