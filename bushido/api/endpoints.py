from fastapi import Request, APIRouter
from fastapi.templating import Jinja2Templates
from fastapi.responses import HTMLResponse


# TODO investigate globel variables
router = APIRouter()
templates = Jinja2Templates(directory='templates/')


@router.get('/', response_class=HTMLResponse)
async def get_index(request: Request):
    return templates.TemplateResponse('index.html', {'request': request})
