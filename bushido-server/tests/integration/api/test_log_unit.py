from unittest.mock import Mock, patch

from fastapi.testclient import TestClient

from bushido_server.schema.res import UnitLogResponse


def test_log_unit(
    client: TestClient,
    session: Mock,
) -> None:
    result = UnitLogResponse(status="OK")

    with patch(
        "bushido_server.api.unit.log_unit",
        return_value=result,
    ) as log_mock:
        response = client.post(
            "/api/unit-logs",
            json={
                "line": "squat 100 5 # test",
            },
        )

    assert response.status_code == 200
    assert response.json() == result.model_dump(mode="json")

    log_mock.assert_called_once_with(
        "squat 100 5 # test",
        session,
    )
