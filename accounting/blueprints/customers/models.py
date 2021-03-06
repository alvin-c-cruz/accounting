from accounting import db
from .. data_model import DataModel


class Customers(db.Model, DataModel):
    id = db.Column(db.Integer, primary_key=True)
    customer_name = db.Column(db.String(64), unique=True, nullable=False)
    customer_tin = db.Column(db.String(16), unique=True, nullable=True)

    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    user = db.relationship('User', backref="customers")

    date_modified = db.Column(db.DateTime, nullable=True)

    def __repr__(self):
        return self.customer_name

    def balance(self):
        from .. sales import Sales
        from .. receipts import Receipts

        run_balance = 0
        for obj in (Sales, Receipts):
            vouchers = obj.query.filter_by(customer_id=self.id).all()

            for voucher in vouchers:
                for entry in voucher.entries:
                    if entry.account.account_type.account_type == "Trade Receivable":
                        run_balance += entry.debit - entry.credit
                        print(entry.account.account_type.account_type)
                        print(entry.debit - entry.credit)

        return run_balance


def customer_choices():
    data = [(row.id, row) for row in Customers.query.order_by(Customers.customer_name).all()]
    data.insert(0, ("", ""))
    return data