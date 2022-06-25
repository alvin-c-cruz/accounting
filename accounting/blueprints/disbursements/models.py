from accounting import db
from .. data_model import DataModel


class Disbursements(db.Model, DataModel):
    id = db.Column(db.Integer, primary_key=True)
    record_date = db.Column(db.DateTime, nullable=False)
    bank_date = db.Column(db.DateTime)
    disbursement_number = db.Column(db.String(32), nullable=False, unique=True)
    check_number = db.Column(db.String(32), nullable=False, unique=True)
    notes = db.Column(db.String(255), nullable=True)

    vendor_id = db.Column(db.Integer, db.ForeignKey("vendors.id"), nullable=False)
    vendor = db.relationship("Vendors", backref="disbursements")

    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    user = db.relationship('User', backref="disbursements")

    date_modified = db.Column(db.DateTime, nullable=True)
    entries = db.relationship("DisbursementsEntry", backref="disbursements")

    def __repr__(self):
        return f"{self.disbursement_number}: {self.vendor_id}"


class DisbursementsEntry(db.Model, DataModel):
    id = db.Column(db.Integer, primary_key=True)
    disbursement_id = db.Column(db.Integer, db.ForeignKey("disbursements.id"), nullable=False)

    account_id = db.Column(db.Integer, db.ForeignKey("accounts.id"), nullable=False)
    account = db.relationship("Accounts", backref="disbursementsentry")

    debit = db.Column(db.Float, default="0.0")
    credit = db.Column(db.Float, default="0.0")

    notes = db.Column(db.String(255))

    def __repr__(self):
        return f"{self.disbursement_id} - {self.account_id}: {self.debit - self.credit}"
