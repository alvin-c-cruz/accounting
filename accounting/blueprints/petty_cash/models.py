from accounting import db
from dataclasses import dataclass
from .. data_model import DataModel


@dataclass
class PettyCash(db.Model, DataModel):
    id = db.Column(db.Integer, primary_key=True)
    record_date = db.Column(db.DateTime, nullable=False)
    report_date = db.Column(db.DateTime)
    petty_cash_number = db.Column(db.String(32), nullable=False, unique=True)
    invoice_number = db.Column(db.String(32), nullable=True)
    notes = db.Column(db.String(255), nullable=True)

    vendor_id = db.Column(db.Integer, db.ForeignKey("vendors.id"), nullable=False)
    vendor = db.relationship("Vendors", backref="pettycash")

    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    user = db.relationship('User', backref="pettycash")

    date_modified = db.Column(db.DateTime, nullable=True)

    def cash_total(self):
        if self.id:
            total = 0
            for entry in self.entries:
                if entry.account.account_type.account_type == "Cash and Cash Equivalents":
                    total += entry.credit
            return "{:,.2f}".format(total)
        else:
            return "0.00"

    def __repr__(self):
        return f"{self.petty_cash_number}: {self.vendor.vendor_name}"


class PettyCashEntry(db.Model, DataModel):
    entry_id = db.Column(db.Integer, primary_key=True)
    petty_cash_id = db.Column(db.Integer, db.ForeignKey("petty_cash.id"), nullable=False)
    petty_cash = db.relationship("PettyCash", backref="entries")

    account_id = db.Column(db.Integer, db.ForeignKey("accounts.id"), nullable=False)
    account = db.relationship("Accounts", backref="pettycashentry")

    debit = db.Column(db.Float, default="0.0")
    credit = db.Column(db.Float, default="0.0")

    notes = db.Column(db.String(255))

    def __repr__(self):
        return f"{self.petty_cash_id} - {self.account_id}: {self.debit - self.credit}"
