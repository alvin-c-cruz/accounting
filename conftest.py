import pytest
from accounting import create_app, db
from accounting.blueprints.user import User
from dataclasses import dataclass


@dataclass
class AdminUser:
    email: str = 'alvinccruz12@gmail.com'
    password: str = 'pbkdf2:sha256:260000$ISdjivpKYjrgigqr$f8ccc9f7e50649308158a7b015339187cc28243c6f66d436720c8f267cb9247a'
    name: str = "Alvin"

    def as_dict(self):
        return {
            "email": self.email,
            "password": self.password,
            "name": self.name
        }


@pytest.fixture(scope="session")
def admin_user():
    return AdminUser

@pytest.fixture(scope="session")
def test_client():
    flask_app = create_app("test_config.py")
    db.init_app(flask_app)
    with flask_app.test_client() as testing_client:
        yield testing_client


@pytest.fixture(scope="session")
def test_client_logged_in():
    flask_app = create_app("test_config.py")
    db.init_app(flask_app)
    with flask_app.test_client() as testing_client:
        testing_client.post('/login', data=AdminUser.as_dict())
        yield testing_client


@pytest.fixture(scope='session')
def init_database(test_client):
    # Create the database and the database table
    with test_client.application.app_context():
        db.create_all()

        # Insert user data
        user = User(
            email=AdminUser.email,
            password=AdminUser.password,
            name=AdminUser.name
        )

        db.session.add(user)

        # Commit the changes for the users
        db.session.commit()

        yield db  # this is where the testing happens!

        db.drop_all()
