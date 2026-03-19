import pytest


def test_get_activities_returns_all_activities(client):
    # Arrange (handled by fixtures)

    # Act
    response = client.get("/activities")

    # Assert
    assert response.status_code == 200
    data = response.json()
    assert "Chess Club" in data
    assert "Programming Class" in data
    assert isinstance(data["Chess Club"]["participants"], list)


def test_signup_adds_participant_and_updates_list(client):
    # Arrange
    activity = "Chess Club"
    new_email = "new_student@mergington.edu"

    # Act
    response = client.post(f"/activities/{activity}/signup", params={"email": new_email})

    # Assert
    assert response.status_code == 200
    assert new_email in response.json()["message"]

    # Verify state updated
    activities = client.get("/activities").json()
    assert new_email in activities[activity]["participants"]


def test_signup_existing_participant_returns_400(client):
    # Arrange
    activity = "Chess Club"
    existing_email = "michael@mergington.edu"

    # Act
    response = client.post(f"/activities/{activity}/signup", params={"email": existing_email})

    # Assert
    assert response.status_code == 400
    assert "already signed up" in response.json()["detail"].lower()


def test_signup_unknown_activity_returns_404(client):
    # Arrange
    unknown_activity = "Not a Real Club"
    email = "student@mergington.edu"

    # Act
    response = client.post(f"/activities/{unknown_activity}/signup", params={"email": email})

    # Assert
    assert response.status_code == 404
    assert "activity not found" in response.json()["detail"].lower()


def test_remove_participant_updates_list(client):
    # Arrange
    activity = "Chess Club"
    removed_email = "michael@mergington.edu"

    # Act
    response = client.delete(f"/activities/{activity}/participants", params={"email": removed_email})

    # Assert
    assert response.status_code == 200
    assert removed_email in response.json()["message"]

    activities = client.get("/activities").json()
    assert removed_email not in activities[activity]["participants"]


def test_remove_nonexistent_participant_returns_404(client):
    # Arrange
    activity = "Chess Club"
    missing_email = "nobody@mergington.edu"

    # Act
    response = client.delete(f"/activities/{activity}/participants", params={"email": missing_email})

    # Assert
    assert response.status_code == 404
    assert "participant not found" in response.json()["detail"].lower()


def test_remove_unknown_activity_returns_404(client):
    # Arrange
    unknown_activity = "Imaginary Club"
    email = "student@mergington.edu"

    # Act
    response = client.delete(f"/activities/{unknown_activity}/participants", params={"email": email})

    # Assert
    assert response.status_code == 404
    assert "activity not found" in response.json()["detail"].lower()
