from accounting import db
from .. data_model import DataModel


class Employees(db.Model, DataModel):
    id = db.Column(db.Integer, primary_key=True)
    employee_name = db.Column(db.String(64), unique=True, nullable=False)
    employee_tin = db.Column(db.String(16), unique=True, nullable=True)

    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    user = db.relationship('User', backref="employees")

    date_modified = db.Column(db.DateTime, nullable=True)

    def __repr__(self):
        return self.employee_name


def employee_choices():
    data = [(row.id, row) for row in Employees.query.order_by(Employees.employee_name).all()]
    data.insert(0, ("", ""))
    return data
