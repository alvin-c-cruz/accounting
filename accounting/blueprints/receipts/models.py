from accounting import db
from dataclasses import dataclass
from .. data_model import DataModel


@dataclass
class Receipts(db.Model, DataModel):
    id = db.Column(db.Integer, primary_key=True)
    record_date = db.Column(db.DateTime, nullable=False)
    bank_date = db.Column(db.DateTime)
    receipt_number = db.Column(db.String(32), nullable=False, unique=True)
    invoice_number = db.Column(db.String(32), nullable=False)
    notes = db.Column(db.String(255), nullable=True)

    customer_id = db.Column(db.Integer, db.ForeignKey("customers.id"), nullable=False)
    customer = db.relationship("Customers", backref="receipts")

    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    user = db.relationship('User', backref="receipts")

    date_modified = db.Column(db.DateTime, nullable=True)

    def cash_total(self):
        if self.id:
            total = 0
            for entry in self.entries:
                if entry.account.account_type.account_type == "Cash and Cash Equivalents":
                    total += entry.debit
            return "{:,.2f}".format(total)
        else:
            return "0.00"

    def __repr__(self):
        return f"{self.receipt_number}: {self.customer.customer_name}"


class ReceiptsEntry(db.Model, DataModel):
    entry_id = db.Column(db.Integer, primary_key=True)
    receipt_id = db.Column(db.Integer, db.ForeignKey("receipts.id"), nullable=False)
    sales = db.relationship("Receipts", backref="entries")

    account_id = db.Column(db.Integer, db.ForeignKey("accounts.id"), nullable=False)
    account = db.relationship("Accounts", backref="receiptsentry")

    debit = db.Column(db.Float, default="0.0")
    credit = db.Column(db.Float, default="0.0")

    notes = db.Column(db.String(255))

    def __repr__(self):
        return f"{self.receipt_id} - {self.account_id}: {self.debit - self.credit}"
