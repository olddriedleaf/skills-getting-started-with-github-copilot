import pytest
from fastapi.testclient import TestClient
from src.app import app

client = TestClient(app)

# Arrange-Act-Assert (AAA) pattern tests for FastAPI endpoints

def test_get_activities_returns_list():
    # Arrange: (No setup needed, uses in-memory data)
    
    # Act
    response = client.get("/activities")
    
    # Assert
    assert response.status_code == 200
    assert isinstance(response.json(), dict)

def test_signup_success():
    # Arrange
    activity_name = "Chess Club"
    email = "student1@example.com"
    
    # Act
    response = client.post(f"/activities/{activity_name}/signup", json={"email": email})
    
    # Assert
    assert response.status_code in (200, 201, 204)
    # Optionally, check if the email is now in the activity's participants
    get_response = client.get("/activities")
    assert email in get_response.json()[activity_name]["participants"]

def test_signup_duplicate():
    # Arrange
    activity_name = "Chess Club"
    email = "student2@example.com"
    client.post(f"/activities/{activity_name}/signup", json={"email": email})
    
    # Act
    response = client.post(f"/activities/{activity_name}/signup", json={"email": email})
    
    # Assert
    assert response.status_code in (400, 409)

def test_signup_nonexistent_activity():
    # Arrange
    activity_name = "Nonexistent Club"
    email = "student3@example.com"
    
    # Act
    response = client.post(f"/activities/{activity_name}/signup", json={"email": email})
    
    # Assert
    assert response.status_code == 404

def test_unregister_success():
    # Arrange
    activity_name = "Chess Club"
    email = "student4@example.com"
    client.post(f"/activities/{activity_name}/signup", json={"email": email})
    
    # Act
    response = client.delete(f"/activities/{activity_name}/unregister", json={"email": email})
    
    # Assert
    assert response.status_code in (200, 204)
    get_response = client.get("/activities")
    assert email not in get_response.json()[activity_name]["participants"]

def test_unregister_nonexistent_activity():
    # Arrange
    activity_name = "Nonexistent Club"
    email = "student5@example.com"
    
    # Act
    response = client.delete(f"/activities/{activity_name}/unregister", json={"email": email})
    
    # Assert
    assert response.status_code == 404

def test_unregister_not_signed_up():
    # Arrange
    activity_name = "Chess Club"
    email = "student6@example.com"
    
    # Act
    response = client.delete(f"/activities/{activity_name}/unregister", json={"email": email})
    
    # Assert
    assert response.status_code in (400, 404)
