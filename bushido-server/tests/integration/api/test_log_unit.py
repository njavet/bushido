from fastapi.testclient import TestClient


def test_log_unit_rejects_empty_line(
    client: TestClient,
) -> None:
    response = client.post(
        "/api/unit-logs",
        json={
            "line": "",
        },
    )

    assert response.status_code == 422
