from fastapi.testclient import TestClient

from del_issue.app import app


def test_create_user(user_dict: dict):
    with TestClient(app) as client:
        response = client.post("/users/", json=user_dict)
        assert response.status_code == 200
        assert response.json()["first_name"] == "John"
        assert response.json()["last_name"] == "Doe"
