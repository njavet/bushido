from collections.abc import Generator
from importlib.resources import files

from sqlalchemy.orm import Session
from fastapi import HTTPException, Path, Request
from fastapi.templating import Jinja2Templates

from bushido.service.mapper.base import UnitMapper
from bushido.service.parser.base import UnitParser
from bushido.core.types import UNIT_T, ORM_T, ORM_ST

templates_dir = files('bushido').joinpath('templates')
templates = Jinja2Templates(directory=str(templates_dir))


def get_templates() -> Jinja2Templates:
    return templates


def get_session(request: Request) -> Generator[Session, None, None]:
    sf = request.app.state.sf
    yield from sf.get_session()


def get_parser(
    request: Request, unit_name: str = Path(...)
) -> UnitParser[UNIT_T]:
    try:
        return request.app.state.parser[unit_name]
    except KeyError:
        raise HTTPException(status_code=404, detail='Unit not found')


def get_mapper(
    request: Request, unit_name: str = Path(...)
) -> UnitMapper[UNIT_T, ORM_T, ORM_ST]:
    try:
        return request.app.state.mapper[unit_name]
    except KeyError:
        raise HTTPException(status_code=404, detail='Unit not found')
