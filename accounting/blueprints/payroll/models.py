from accounting import db
from dataclasses import dataclass
from .. data_model import DataModel


@dataclass
class Payroll(db.Model, DataModel):
    id = db.Column(db.Integer, primary_key=True)
    record_date = db.Column(db.DateTime, nullable=False)
    payroll_number = db.Column(db.String(32), nullable=False, unique=True)
    notes = db.Column(db.String(255), nullable=True)

    employee_id = db.Column(db.Integer, db.ForeignKey("employees.id"), nullable=False)
    employee = db.relationship("Employees", backref="payrolls")

    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    user = db.relationship('User', backref="payrolls")

    date_modified = db.Column(db.DateTime, nullable=True)

    def cash_total(self):
        if self.id:
            total = 0
            for entry in self.entries:
                if entry.account.account_title == "Salaries Payable":
                    total += entry.credit
            return "{:,.2f}".format(total)
        else:
            return "0.00"

    def __repr__(self):
        return f"{self.payroll_number}: {self.employee.employee_name}"


class PayrollEntry(db.Model, DataModel):
    entry_id = db.Column(db.Integer, primary_key=True)
    payroll_id = db.Column(db.Integer, db.ForeignKey("payroll.id"), nullable=False)
    payroll = db.relationship("Payroll", backref="entries")

    account_id = db.Column(db.Integer, db.ForeignKey("accounts.id"), nullable=False)
    account = db.relationship("Accounts", backref="payrollentry")

    debit = db.Column(db.Float, default="0.0")
    credit = db.Column(db.Float, default="0.0")

    notes = db.Column(db.String(255))

    def __repr__(self):
        return f"{self.payroll_id} - {self.account_id}: {self.debit - self.credit}"
