from importlib.resources import files
from typing import Any, Generator, Mapping, cast

from fastapi import HTTPException, Path, Request
from fastapi.templating import Jinja2Templates
from sqlalchemy.orm import Session

from bushido.core.types import ORM_T
from bushido.iface.mapper.unit import UnitMapper
from bushido.iface.parser.unit import UnitParser
from bushido.infra.repo.unit import UnitRepo

templates_dir = files('bushido').joinpath('templates')
templates = Jinja2Templates(directory=str(templates_dir))


def get_templates() -> Jinja2Templates:
    return templates


def get_session(request: Request) -> Generator[Session, None, None]:
    sf = request.app.state.sf
    yield from sf.get_session()

