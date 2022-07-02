from accounting import db
from .. data_model import DataModel


class Vendors(db.Model, DataModel):
    id = db.Column(db.Integer, primary_key=True)
    vendor_name = db.Column(db.String(64), unique=True, nullable=False)
    vendor_tin = db.Column(db.String(16), unique=True, nullable=True)

    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    user = db.relationship('User', backref="vendors")

    date_modified = db.Column(db.DateTime, nullable=True)

    def __repr__(self):
        return self.vendor_name


def vendor_choices():
    data = [(row.id, row) for row in Vendors.query.order_by(Vendors.vendor_name).all()]
    data.insert(0, ("", ""))
    return data