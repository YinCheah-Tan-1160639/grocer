import pytest
from database import db
from models import Person  # Import your Person model
from flask import session

@pytest.fixture
def add_test_user(app):
    # Add a sample user to the database
    with app.app_context():
        user = Person(username="test_user", password="hashed_password")
        db.session.add(user)
        db.session.commit()

def test_login_successful(client, user):
    # Login with the correct password
    response = client.post('/login', data={'username': 'test_user', 'password': 'hashed_password'})
    
    # Assert redirect to the dashboard
    assert response.status_code == 302
    assert response.headers["Location"] == "/dashboard"
    
    # Check that the user ID and role are stored in the session
    with client.session_transaction() as sess:
        assert 'user_id' in sess
        assert sess['username'] == 'test_user'

def test_login_failed(client, add_test_user):
    # Attempt login with incorrect password
    response = client.post('/login', data={'username': 'test_user', 'password': 'wrong_password'})
    
    # Check for a redirect back to the login page and a flash message
    assert response.status_code == 302
    assert response.headers["Location"] == "/login"
    assert b"Invalid username or password!" in response.data  # Check for the flash message