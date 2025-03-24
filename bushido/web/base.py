from fastapi import Request, APIRouter, Depends
from fastapi.templating import Jinja2Templates
from fastapi.responses import HTMLResponse

# project imports
from bushido.service.base import BaseService
from bushido.service.categories.category import InputProcessor


# TODO investigate global variables
router = APIRouter()
templates = Jinja2Templates(directory='templates/')
bs = BaseService()
ip = InputProcessor(bs.load_processors())


@router.get('/', response_class=HTMLResponse)
async def get_index(request: Request):
    dix = bs.construct_autocomplete_dix()
    return templates.TemplateResponse('index.html',
                                      {'request': request,
                                       'autocomp': dix})


@router.post('/log_unit')
async def log_unit(request: Request):
    data = await request.json()
    print('data', data)
    ip.preprocess_input()
