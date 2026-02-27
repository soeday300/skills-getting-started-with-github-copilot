from fastapi.testclient import TestClient
from src.app import app, activities

client = TestClient(app)


def setup_function():
    # reset in-memory data before each test
    activities.clear()
    activities.update({
        "Test Activity": {
            "description": "A dummy activity",
            "schedule": "Now",
            "max_participants": 2,
            "participants": []
        }
    })


def test_get_activities():
    # Arrange: setup handled by setup_function, nothing extra
    # Act
    response = client.get("/activities")
    # Assert
    assert response.status_code == 200
    data = response.json()
    assert "Test Activity" in data


def test_signup_and_duplicate_prevention():
    # Arrange: test activity exists via setup_function
    # Act & Assert: first signup works
    resp1 = client.post("/activities/Test Activity/signup", params={"email": "a@b.com"})
    assert resp1.status_code == 200
    assert resp1.json()["message"] == "Signed up a@b.com for Test Activity"

    # Act & Assert: duplicate signup should fail
    resp2 = client.post("/activities/Test Activity/signup", params={"email": "a@b.com"})
    assert resp2.status_code == 400
    assert "already signed up" in resp2.json()["detail"]

    # Act & Assert: another student allowed
    resp3 = client.post("/activities/Test Activity/signup", params={"email": "c@d.com"})
    assert resp3.status_code == 200

    # Act & Assert: hitting capacity
    resp4 = client.post("/activities/Test Activity/signup", params={"email": "e@f.com"})
    assert resp4.status_code == 400
    assert "is full" in resp4.json()["detail"]


def test_remove_participant():
    # Arrange: sign up two participants
    client.post("/activities/Test Activity/signup", params={"email": "x@y.com"})
    client.post("/activities/Test Activity/signup", params={"email": "z@w.com"})
    assert "x@y.com" in activities["Test Activity"]["participants"]

    # Act: remove one
    resp = client.delete("/activities/Test Activity/participants", params={"email": "x@y.com"})
    # Assert removal success
    assert resp.status_code == 200
    assert "Unregistered x@y.com" in resp.json()["message"]
    assert "x@y.com" not in activities["Test Activity"]["participants"]

    # Act & Assert: removing non-existent yields 404
    resp2 = client.delete("/activities/Test Activity/participants", params={"email": "nope@none"})
    assert resp2.status_code == 404


def test_nonexistent_activity():
    resp = client.post("/activities/Nope/signup", params={"email": "a@b.com"})
    assert resp.status_code == 404
    resp2 = client.delete("/activities/Nope/participants", params={"email": "a@b.com"})
    assert resp2.status_code == 404
