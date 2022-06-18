from flask_sqlalchemy import SQLAlchemy
from flask_mail import Mail
from flask_bcrypt import Bcrypt

db = SQLAlchemy()
mail = Mail()
bcrypt = Bcrypt()