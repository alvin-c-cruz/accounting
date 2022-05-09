import os
from flask import Flask,redirect, url_for, abort, request
from flask_login import LoginManager
from http import HTTPStatus
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_mail import Mail
from flask_bcrypt import Bcrypt

db = SQLAlchemy()
mail = Mail()
bcrypt = Bcrypt()

from . import blueprints


def create_app(test_config=None):
    app = Flask(__name__, instance_relative_config=True)

    if test_config is None:
        app.config.from_pyfile(os.path.join(app.instance_path, "config.py"))
    else:
        app.config.from_pyfile(os.path.join(app.instance_path, test_config))
        app.config ['SQLALCHEMY_DATABASE_URI'] = "sqlite:///" + os.path.join(app.instance_path, "data.db")
        app.config ['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
        print(test_config)

    if not os.path.isdir(app.instance_path):
        os.makedirs(app.instance_path)

    login_manager = LoginManager()
    login_manager.init_app(app)

    @login_manager.user_loader
    def load_user(user_id):
        return blueprints.user.User.query.get(user_id)

    @login_manager.unauthorized_handler
    def unauthorized():
        if request.blueprint == 'api':
            abort(HTTPStatus.UNAUTHORIZED)
        return redirect(url_for('landing_page.home'))

    for module_ in dir(blueprints):
        module_obj = getattr(blueprints, module_)
        if hasattr(module_obj, 'bp'):
            app.register_blueprint(getattr(module_obj, 'bp'))

    bcrypt.init_app(app)
    mail.init_app(app)

    db.init_app(app)
    Migrate(app, db)

    return app
