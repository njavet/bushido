from fastapi import Request, APIRouter, Depends
from fastapi.templating import Jinja2Templates
from fastapi.responses import HTMLResponse

# project imports
from bushido.data.base import DatabaseManager
from bushido.service.base import BaseService


# TODO investigate global variables
router = APIRouter()
templates = Jinja2Templates(directory='templates/')


@router.get('/emojis')
async def fetch_emojis(dbm: DatabaseManager = Depends(dbm)):
    pass



@router.get('/', response_class=HTMLResponse)
async def get_index(request: Request):
    dix = base_service.construct_autocomplete_dix()
    return templates.TemplateResponse('index.html',
                                      {'request': request,
                                       'autocomp': dix})


@router.post('/log_unit')
async def log_unit(request: Request):
    data = await request.json()
    print('data', data)
