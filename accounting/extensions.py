from flask_sqlalchemy import SQLAlchemy
from flask_mail import Mail
from flask_bcrypt import Bcrypt

db = SQLAlchemy()
mail = Mail()
bcrypt = Bcrypt()


def incrementer(data):
    if not data:
        return 1

    if type(data) is int:
        return data + 1

    if data.isdigit():
        return str(int(data) + 1).rjust(len(data), '0')

    # Upon passing this line the data passed is alphanumeric combination
    reversed_data = data[::-1]
    reversed_number = ""
    for i in reversed_data:
        if i.isdigit():
            reversed_number += i
        else:
            break
    proper_number = reversed_number[::-1]

    if proper_number:
        return data[:len(data) - len(proper_number)] + str(int(proper_number) + 1).rjust(
            len(proper_number), '0')
    else:
        return data + "1"


def to_float(data):
    if type(data) not in (int, float):
        data = data.replace(",", "")
        data = data.replace("-", "")
        if not data.isdigit():
            return 0
    return float(data)


def balance_check(entries):
    total_debit = 0
    total_credit = 0
    for entry in entries:
        total_debit += to_float(entry.debit.data)
        total_credit += to_float(entry.credit.data)

    return round(total_debit, 2), round(total_credit, 2)
