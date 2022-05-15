import pytest
from accounting import create_app, db
from accounting.blueprints.user import User


@pytest.fixture(scope="session")
def client():
    app = create_app(test_config="test_config.py")
    db.init_app(app)
    return app.test_client()


@pytest.fixture(scope='session')
def init_database(client):
    # Create the database and the database table
    with client.application.app_context():
        db.create_all()

        # Insert user data
        user = User(
            email='alvinccruz12@gmail.com',
            password='pbkdf2:sha256:260000$ISdjivpKYjrgigqr$f8ccc9f7e50649308158a7b015339187cc28243c6f66d436720c8f267cb9247a',
            name="Alvin"
        )

        db.session.add(user)

        # Commit the changes for the users
        db.session.commit()

        yield db  # this is where the testing happens!

        db.drop_all()
