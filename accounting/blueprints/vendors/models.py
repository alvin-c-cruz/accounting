from accounting import db
from .. data_model import DataModel


class Vendors(db.Model, DataModel):
    __tablename__ = "tbl_vendors"
    page_title = "Vendor"
    add_label = "Add Vendor"
    edit_label = "Edit Vendor"

    vendor_name = db.Column(db.String(64), unique=True, nullable=False)
    vendor_tin = db.Column(db.String(16), unique=True, nullable=True)

    user_id = db.Column(db.Integer, db.ForeignKey('tbl_user.id'), nullable=False)
    user = db.relationship('User', backref=db.backref(__tablename__, lazy=True))

    date_modified = db.Column(db.DateTime, nullable=True)

    def __repr__(self):
        return self.vendor_name
