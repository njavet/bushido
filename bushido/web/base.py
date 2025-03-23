from fastapi import Request, APIRouter
from fastapi.templating import Jinja2Templates
from fastapi.responses import HTMLResponse

# project imports


# TODO investigate global variables
router = APIRouter()
templates = Jinja2Templates(directory='templates/')


@router.get('/', response_class=HTMLResponse)
async def get_index(request: Request):
    return templates.TemplateResponse('index.html',
                                      {'request': request})


@router.post('/log_unit')
async def log_unit(request: Request):
    data = await request.json()
    print('data', data)
