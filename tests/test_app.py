from fastapi.testclient import TestClient

from src.app import activities, app

client = TestClient(app)


def test_unregister_participant_removes_email_from_activity():
    # Arrange
    activity = activities["Chess Club"]
    activity["participants"] = ["michael@mergington.edu", "daniel@mergington.edu"]

    # Act
    response = client.delete("/activities/Chess Club/participants/michael@mergington.edu")

    # Assert
    assert response.status_code == 200
    assert response.json() == {
        "message": "Unregistered michael@mergington.edu from Chess Club"
    }
    assert "michael@mergington.edu" not in activity["participants"]
    assert "daniel@mergington.edu" in activity["participants"]


def test_unregister_participant_returns_404_for_missing_activity():
    # Arrange
    # No setup needed for a missing activity.

    # Act
    response = client.delete("/activities/Does Not Exist/participants/test@example.com")

    # Assert
    assert response.status_code == 404
    assert response.json()["detail"] == "Activity not found"


def test_unregister_participant_returns_400_for_missing_email():
    # Arrange
    activity = activities["Chess Club"]
    activity["participants"] = ["daniel@mergington.edu"]

    # Act
    response = client.delete("/activities/Chess Club/participants/ghost@example.com")

    # Assert
    assert response.status_code == 400
    assert response.json()["detail"] == "Participant not found for this activity"
