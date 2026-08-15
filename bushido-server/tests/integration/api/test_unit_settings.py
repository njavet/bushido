from unittest.mock import Mock, patch

from fastapi.testclient import TestClient

from bushidolib.constants import UnitCategory
from bushidolib.unit import UnitSetting


def test_get_unit_settings(
    client: TestClient,
    session: Mock,
) -> None:
    settings = [
        UnitSetting(
            name="squat",
            category=UnitCategory.LIFTING,
        ),
        UnitSetting(
            name="running",
            category=UnitCategory.CARDIO,
        ),
    ]

    with patch(
        "bushido_server.api.unit.load_unit_mappings",
        return_value=settings,
    ) as load_mock:
        response = client.get("/api/unit-settings")

    assert response.status_code == 200
    assert response.json() == [
        {
            "name": "squat",
            "category": "lifting",
        },
        {
            "name": "running",
            "category": "cardio",
        },
    ]

    load_mock.assert_called_once_with(session)
