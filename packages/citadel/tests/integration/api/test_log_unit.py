from fastapi.testclient import TestClient


def test_log_unit_rejects_empty_line(client: TestClient) -> None:
    response = client.post(
        "/api/unit-logs",
        json={
            "line": "",
        },
    )
    assert response.status_code == 422


def test_log_lifting_unit(client: TestClient) -> None:
    response = client.post(
        "/api/unit-logs",
        json={
            "line": "squat 0 120 5 # yo",
        },
    )
    assert response.status_code == 200, response.text
