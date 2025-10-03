from importlib.resources import files
from typing import Generator

from fastapi import Request
from fastapi.templating import Jinja2Templates
from sqlalchemy.orm import Session

templates_dir = files('bushido').joinpath('templates')
templates = Jinja2Templates(directory=str(templates_dir))


def get_templates() -> Jinja2Templates:
    return templates


def get_session(request: Request) -> Generator[Session, None, None]:
    sf = request.app.state.sf
    yield from sf.get_session()
