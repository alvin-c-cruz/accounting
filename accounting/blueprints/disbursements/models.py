from accounting import db
from .. data_model import DataModel


class Disbursements(db.Model, DataModel):
    __tablename__ = "tbl_disbursements"

    page_title = "Check Disbursements"
    add_label = "Add Check Disbursement"
    edit_label = "Edit Check Disbursement"

    record_date = db.Column(db.DateTime, nullable=False)
    bank_date = db.Column(db.DateTime, nullable=True)
    disbursement_number = db.Column(db.String(32), nullable=False, unique=True)
    check_number = db.Column(db.String(32), nullable=False, unique=True)
    notes = db.Column(db.String(255), nullable=True)

    vendor_id = db.Column(db.Integer, db.ForeignKey("tbl_vendors.id"), nullable=False)
    vendor = db.relationship("Vendors", backref=db.backref(__tablename__, lazy=True))

    user_id = db.Column(db.Integer, db.ForeignKey('tbl_user.id'), nullable=False)
    user = db.relationship('User', backref=db.backref(__tablename__, lazy=True))

    def __repr__(self):
        return f"{self.disbursement_number}: {self.vendor_id}"


class DisbursementsEntry(db.Model, DataModel):
    __tablename__ = "tbl_disbursements_entry"

    disbursement_id = db.Column(db.Integer, db.ForeignKey("tbl_disbursements.id"), nullable=False)
    disbursement = db.relationship("Disbursements", backref=db.backref(__tablename__, lazy=True))

    account_id = db.Column(db.Integer, db.ForeignKey("tbl_accounts.id"), nullable=False)
    account = db.relationship("Accounts", backref=db.backref(__tablename__, lazy=True))

    debit = db.Column(db.Float, default="0.0")
    credit = db.Column(db.Float, default="0.0")

    notes = db.Column(db.String(255), nullable=False)

    def __repr__(self):
        return f"{self.disbursement} - {self.account_id}: {self.debit - self.credit}"