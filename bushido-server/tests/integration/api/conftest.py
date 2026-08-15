from collections.abc import Generator
from unittest.mock import Mock

import pytest
from fastapi import FastAPI
from fastapi.testclient import TestClient
from sqlalchemy.orm import Session

from bushido_server.api import router
from bushido_server.api.deps import get_session


@pytest.fixture
def session() -> Mock:
    return Mock(spec=Session)


@pytest.fixture
def app(session: Mock) -> FastAPI:
    app = FastAPI()
    app.include_router(router)

    def override_get_session() -> Generator[Session]:
        yield session

    app.dependency_overrides[get_session] = override_get_session
    return app


@pytest.fixture
def client(app: FastAPI) -> TestClient:
    return TestClient(app)
