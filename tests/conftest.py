import pytest
from resume_builder import create_app, db
from resume_builder.models import User


@pytest.fixture(scope="module")
def test_app():
    """Create and configure a new app instance for each test."""
    app = create_app()
    app.config.update(
        {
            "TESTING": True,
            "SQLALCHEMY_DATABASE_URI": "sqlite:///:memory:",
            "WTF_CSRF_ENABLED": False,  # Disable CSRF for testing forms
            "SECRET_KEY": "test",
        }
    )

    with app.app_context():
        db.create_all()
        yield app
        db.drop_all()


@pytest.fixture(scope="module")
def test_client(test_app):
    """A test client for the app."""
    return test_app.test_client()


@pytest.fixture(scope="function")
def new_user(test_app):
    """Fixture to create a new user for tests."""
    with test_app.app_context():
        user = User(username="testusername")
        user.set_password("password")
        db.session.add(user)
        db.session.commit()
        yield user
        db.session.delete(user)
        db.session.commit()
