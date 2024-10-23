# tests/test_main.py

import os
import sys
from fastapi.testclient import TestClient
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../app')))
from main import app 

client = TestClient(app)

# Tests for the user registration endpoint
def test_register_user():
    response = client.post("/register/", json={"username": "testuser", "email": "test@example.com"})
    assert response.status_code == 200
    assert response.json() == {"username": "testuser", "email": "test@example.com"}

    # Attempt to register the same user again
    response = client.post("/register/", json={"username": "testuser", "email": "test@example.com"})
    assert response.status_code == 400
    assert response.json() == {"detail": "User already registered"}

# Tests for the user retrieval endpoint
def test_get_user():
    # First, register the user
    client.post("/register/", json={"username": "testuser2", "email": "test2@example.com"})

    response = client.get("/users/testuser2")
    assert response.status_code == 200
    assert response.json() == {"username": "testuser2", "email": "test2@example.com"}

    # Attempt to retrieve a non-existent user
    response = client.get("/users/nonexistentuser")
    assert response.status_code == 404
    assert response.json() == {"detail": "User not found"}

# Tests for the user deletion endpoint
def test_delete_user():
    # First, register the user
    client.post("/register/", json={"username": "testuser3", "email": "test3@example.com"})

    response = client.delete("/users/testuser3")
    assert response.status_code == 200
    assert response.json() == {"detail": "User deleted"}

    # Attempt to delete a non-existent user
    response = client.delete("/users/nonexistentuser")
    assert response.status_code == 404
    assert response.json() == {"detail": "User not found"}
