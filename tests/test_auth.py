import pytest
from app import app
from config.db import mongo
from werkzeug.security import generate_password_hash

@pytest.fixture
def client():
    """Fixture to create a test client for the Flask app."""
    app.config["TESTING"] = True
    app.config["MONGO_URI"] = "mongodb://localhost:27017/test_userdb"
    with app.test_client() as client:
        with app.app_context():
            mongo.init_app(app)
            # Clear the test database before running tests
            mongo.db.users.delete_many({})
        yield client

def test_signup_success(client):
    """Test successful user signup."""
    response = client.post("/api/auth/signup", json={"email": "test@example.com", "password": "password123"})
    assert response.status_code == 201
    assert response.json["message"] == "User created successfully"

def test_signup_user_exists(client):
    """Test signup when user already exists."""
    # Pre-insert a user
    mongo.db.users.insert_one({
        "email": "existing@example.com",
        "password": generate_password_hash("password123")
    })
    response = client.post("/api/auth/signup", json={"email": "existing@example.com", "password": "password123"})
    assert response.status_code == 409
    assert response.json["error"] == "User already exists"

def test_login_success(client):
    """Test successful login."""
    # Pre-insert a user
    mongo.db.users.insert_one({
        "email": "login@example.com",
        "password": generate_password_hash("password123")
    })
    response = client.post("/api/auth/login", json={"email": "login@example.com", "password": "password123"})
    assert response.status_code == 200
    assert "access_token" in response.json

def test_login_invalid_credentials(client):
    """Test login with invalid credentials."""
    # Pre-insert a user
    mongo.db.users.insert_one({
        "email": "invalid@example.com",
        "password": generate_password_hash("password123")
    })
    # Attempt login with incorrect password
    response = client.post("/api/auth/login", json={"email": "invalid@example.com", "password": "wrongpassword"})
    assert response.status_code == 401
    assert response.json["error"] == "Invalid email or password"

def test_login_user_not_found(client):
    """Test login for non-existent user."""
    response = client.post("/api/auth/login", json={"email": "nonexistent@example.com", "password": "password123"})
    assert response.status_code == 401
    assert response.json["error"] == "Invalid email or password"
