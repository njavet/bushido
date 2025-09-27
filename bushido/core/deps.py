from importlib.resources import files
from typing import Any, Generator, Mapping, cast

from fastapi import HTTPException, Path, Request
from fastapi.templating import Jinja2Templates
from sqlalchemy.orm import Session

from bushido.iface.mapper.base import UnitMapper
from bushido.iface.parser.base import UnitParser

templates_dir = files('bushido').joinpath('templates')
templates = Jinja2Templates(directory=str(templates_dir))


def get_templates() -> Jinja2Templates:
    return templates


def get_session(request: Request) -> Generator[Session, None, None]:
    sf = request.app.state.sf
    yield from sf.get_session()


def get_parser(
    request: Request, unit_name: str = Path(...)
) -> UnitParser[Any]:
    # TODO remove quick mypy fix
    parsers = cast(Mapping[str, UnitParser[Any]], request.app.state.parsers)
    try:
        return parsers[unit_name]
    except KeyError:
        raise HTTPException(status_code=404, detail='Unit not found')


def get_mapper(
    request: Request, unit_name: str = Path(...)
) -> UnitMapper[Any, Any, Any]:
    # TODO remove quick mypy fix
    mappers = cast(
        Mapping[str, UnitMapper[Any, Any, Any]], request.app.state.mappers
    )
    try:
        return mappers[unit_name]
    except KeyError:
        raise HTTPException(status_code=404, detail='Unit not found')
