from fastapi import Request, APIRouter
from fastapi.templating import Jinja2Templates
from fastapi.responses import HTMLResponse
from datetime import datetime

# project imports
from bushido.data.db_manager import DatabaseManager


# TODO investigate global variables
router = APIRouter()
templates = Jinja2Templates(directory='templates/')
dbm = DatabaseManager(db_url='sqlite:///bushido.db')


@router.get('/', response_class=HTMLResponse)
async def get_index(request: Request):
    dix = dbm.get_date2units()
    return templates.TemplateResponse('index.html',
                                      {'request': request,
                                       'dix': dix})

