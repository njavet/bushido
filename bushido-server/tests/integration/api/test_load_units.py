import datetime
from unittest.mock import Mock, patch

from fastapi.testclient import TestClient

from bushidolib.constants import UnitCategory
from bushidolib.lifting import LiftingData, LiftingSetData, LiftingUnit


def test_query_units(
    client: TestClient,
    session: Mock,
) -> None:
    units = [
        LiftingUnit(
            name="squat",
            log_time=datetime.datetime(
                2026,
                8,
                15,
                12,
                0,
                tzinfo=datetime.UTC,
            ),
            comment=None,
            data=LiftingData(
                program=None,
                variant=None,
                sets=[
                    LiftingSetData(set_nr=0, weight=128.0, reps=8, rest=180.0),
                    LiftingSetData(set_nr=1, weight=128.0, reps=8, rest=0.0),
                ],
            ),
        ),
    ]

    with patch(
        "bushido_server.api.unit.load_units",
        return_value=units,
    ) as load_mock:
        response = client.post(
            "/api/unit-logs/query",
            json={
                "unit_category": "lifting",
            },
        )

    assert response.status_code == 200
    assert response.json() == [unit.model_dump(mode="json") for unit in units]

    request = load_mock.call_args.args[0]

    assert request.unit_category is UnitCategory.LIFTING

    assert load_mock.call_args.args[1] is session


def test_query_units_rejects_invalid_category(
    client: TestClient,
) -> None:
    response = client.post(
        "/api/unit-logs/query",
        json={
            "unit_category": "nuclear_kata",
            "start_time": None,
            "end_time": None,
        },
    )

    assert response.status_code == 422
