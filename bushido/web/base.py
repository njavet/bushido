from fastapi import Request, APIRouter, Depends
from fastapi.templating import Jinja2Templates
from fastapi.responses import HTMLResponse, JSONResponse

# project imports
from bushido.service.base import BaseService
from bushido.service.categories.category import InputProcessor


# TODO investigate global variables
router = APIRouter()
templates = Jinja2Templates(directory='templates/')
bs = BaseService()
ip = InputProcessor(bs.load_processors())


@router.get('/emojis')
async def fetch_emojis():
    return bs.construct_autocomplete_list()


@router.get('/', response_class=HTMLResponse)
async def get_index(request: Request):
    return templates.TemplateResponse('index.html',
                                      {'request': request})


@router.post('/log_unit')
async def log_unit(request: Request):
    data = await request.json()
    print('data', data)
    answer = ip.preprocess_input(data['text'])
    print('answer', answer)
    return {'answer': answer}
