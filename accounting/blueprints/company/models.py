from accounting import db
from .. data_model import DataModel


class Company(db.Model, DataModel):
    id = db.Column(db.Integer, primary_key=True)
    company_name = db.Column(db.String(64))

    disbursement_prepared = db.Column(db.String(32), default="")
    disbursement_check = db.Column(db.String(32), default="")
    disbursement_audited = db.Column(db.String(32), default="")
    disbursement_approved = db.Column(db.String(32), default="")
