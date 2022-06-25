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