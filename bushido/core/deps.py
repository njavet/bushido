from importlib.resources import files
from fastapi import Query
from fastapi.templating import Jinja2Templates

# project imports
from bushido.core.app_context import app_context


templates_dir = files("bushido").joinpath("templates")
templates = Jinja2Templates(directory=str(templates_dir))


def get_templates():
    return templates


def get_session(db_instance: str = Query(...)):
    sf = app_context.dbs[db_instance]
    yield from sf.get_session()
