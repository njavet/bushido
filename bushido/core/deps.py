from importlib.resources import files

from fastapi import Request, Path, HTTPException
from fastapi.templating import Jinja2Templates

from bushido.service.mapper.base import UnitMapper
from bushido.service.parser.base import UnitParser


templates_dir = files('bushido').joinpath('templates')
templates = Jinja2Templates(directory=str(templates_dir))


def get_templates():
    return templates


def get_session(request: Request):
    sf = request.app.state.sf
    yield from sf.get_session()


def get_parser(request: Request, unit_name: str = Path(...)) -> UnitParser:
    try:
        return request.app.state.parser[unit_name]
    except KeyError:
        raise HTTPException(status_code=404, detail='Unit not found')


def get_mapper(request: Request, unit_name: str = Path(...)) -> UnitMapper:
    try:
        return request.app.state.mapper[unit_name]
    except KeyError:
        raise HTTPException(status_code=404, detail='Unit not found')
