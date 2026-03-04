
import pytest
from fastapi.testclient import TestClient
from src.app import app

import asyncio


# Test root endpoint (AAA pattern)
def test_root_endpoint():
    # Arrange: create test client
    client = TestClient(app)
    # Act: make GET request to root
    response = client.get("/")
    # Assert: check redirect
    assert response.status_code == 200 or response.status_code == 307

# Test GET /activities (AAA pattern)
def test_get_activities():
    # Arrange: create test client
    client = TestClient(app)
    # Act: get activities
    response = client.get("/activities")
    # Assert: check response
    assert response.status_code == 200
    data = response.json()
    assert isinstance(data, dict)
    assert "Chess Club" in data

# Test POST /activities/{activity_name}/signup success (AAA pattern)
def test_signup_for_activity_success():
    # Arrange: set up activity and email
    client = TestClient(app)
    activity = "Art Club"
    email = "testuser@mergington.edu"
    # Act: sign up for activity
    response = client.post(f"/activities/{activity}/signup", params={"email": email})
    # Assert: check signup success
    assert response.status_code == 200
    assert response.json()["message"] == f"Signed up {email} for {activity}"

# Test POST /activities/{activity_name}/signup for non-existent activity (AAA pattern)
def test_signup_for_activity_not_found():
    # Arrange: set up non-existent activity
    client = TestClient(app)
    activity = "Nonexistent Club"
    email = "testuser@mergington.edu"
    # Act: try to sign up
    response = client.post(f"/activities/{activity}/signup", params={"email": email})
    # Assert: check not found error
    assert response.status_code == 404
    assert response.json()["detail"] == "Activity not found"

# Test POST /activities/{activity_name}/signup for already signed up student (AAA pattern)
def test_signup_for_activity_already_signed_up():
    # Arrange: use already signed up student
    client = TestClient(app)
    activity = "Chess Club"
    email = "michael@mergington.edu"  # Already signed up
    # Act: try to sign up again
    response = client.post(f"/activities/{activity}/signup", params={"email": email})
    # Assert: check already signed up error
    assert response.status_code == 400
    assert response.json()["detail"] == "Student already signed up"
