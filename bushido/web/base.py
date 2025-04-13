from fastapi import Request, APIRouter
from fastapi.responses import HTMLResponse

# project imports
from bushido.service.setup import setup_dm


router = APIRouter()


@router.get('/', response_class=HTMLResponse)
async def index(request: Request):
    templates = request.app.state.templates
    return templates.TemplateResponse('index.html', {'request': request})

