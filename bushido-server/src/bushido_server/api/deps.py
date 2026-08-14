from collections.abc import Generator
from typing import Annotated

from fastapi import Depends, Request
from sqlalchemy.orm import Session


def get_session(request: Request) -> Generator[Session]:
    sf = request.app.state.sf
    with sf.session() as session:
        yield session


SessionDep = Annotated[Session, Depends(get_session)]
