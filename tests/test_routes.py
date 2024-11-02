import pytest
from flask import session
from app import create_app  # Adjust this import based on how your app is structured
from models import Person  # Adjust the import to match your model

@pytest.fixture
def app():
    # Create and configure a new app instance for each test
    app = create_app('testing')  # Ensure you have a testing config
    yield app

@pytest.fixture
def client(app):
    # Create a test client for the app
    return app.test_client()

@pytest.fixture
def init_db():
    # Initialize the database and create a test user
    with app.app_context():
        # Create database tables, insert test data
        Person.create(username='testuser', password='testpass', role='customer')
        yield
        # Cleanup after tests (e.g., drop the test database)

def test_index(client):
    response = client.get('/')
    assert b'Welcome' in response.data  # Change 'Welcome' to text you expect

def test_login(client, init_db):
    response = client.post('/login', data={'username': 'testuser', 'password': 'testpass'})
    with client.session_transaction() as sess:
        assert 'user_id' in sess
        assert sess['username'] == 'testuser'
        assert sess['role'] == 'customer'
    assert response.status_code == 302  # Check for redirect
    assert response.location == 'http://localhost/dashboard'  # Update as needed

def test_login_invalid(client):
    response = client.post('/login', data={'username': 'wronguser', 'password': 'wrongpass'})
    with client.session_transaction() as sess:
        assert 'user_id' not in sess
    assert response.status_code == 302  # Check for redirect
    assert response.location == 'http://localhost/login'  # Update as needed

def test_dashboard(client, init_db):
    client.post('/login', data={'username': 'testuser', 'password': 'testpass'})  # Log in first
    response = client.get('/dashboard')
    assert response.status_code == 200
    assert b'Dashboard' in response.data  # Change to text you expect

def test_logout(client, init_db):
    client.post('/login', data={'username': 'testuser', 'password': 'testpass'})  # Log in first
    response = client.get('/logout')
    with client.session_transaction() as sess:
        assert 'user_id' not in sess
    assert response.status_code == 302  # Check for redirect
    assert response.location == 'http://localhost/login'  # Update as needed