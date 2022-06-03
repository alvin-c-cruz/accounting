from accounting import db
from .. data_model import DataModel


class Vendors(db.Model, DataModel):
    __tablename__ = "tbl_vendors"
    page_title = "Vendor"
    add_label = "Add Vendor"
    edit_label = "Edit Vendor"

    vendor_name = db.Column(db.String(64), unique=True, nullable=False)
    vendor_tin = db.Column(db.String(16), unique=True, nullable=True)

    def __repr__(self):
        return self.vendor_name

