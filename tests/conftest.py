import pytest
from app import create_app
from database import db

@pytest.fixture
def app():
    app = create_app()
    app.config.update({
        "TESTING": True,
        "SQLALCHEMY_DATABASE_URI": "sqlite:///:memory:"  # Use an in-memory database for tests
    })

    with app.app_context():
        db.create_all()  # Create tables
        yield app
        db.drop_all()  # Clean up after tests

@pytest.fixture
def client(app):
    return app.test_client()