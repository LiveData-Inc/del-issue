from fastapi.testclient import TestClient


def test_create_user(client: TestClient, user_dict: dict):
    response = client.post("/users/", json=user_dict)
    assert response.status_code == 200
    assert response.json()["first_name"] == "John"
    assert response.json()["last_name"] == "Doe"
    assert response.json()["last_name"] == "Doe"
