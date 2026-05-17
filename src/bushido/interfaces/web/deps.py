from typing import Generator

from fastapi import Request
from sqlalchemy.orm import Session


def get_session(request: Request) -> Generator[Session, None, None]:
    sf = request.app.state.sf
    yield from sf.get_session()
