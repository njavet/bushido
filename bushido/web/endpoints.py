from fastapi import Request, APIRouter
from fastapi.templating import Jinja2Templates
from fastapi.responses import HTMLResponse
from babel.dates import format_date
from datetime import datetime

# project imports
from bushido.utils.dt_functions import get_datetime_from_timestamp
from bushido.data.db_manager import DatabaseManager


# TODO investigate global variables
router = APIRouter()
templates = Jinja2Templates(directory='templates/')
templates.env.filters['format_datetime'] = format_date
templates.env.filters['timezone'] = get_datetime_from_timestamp
dbm = DatabaseManager(db_url='sqlite:///bushido.db')



@router.get('/', response_class=HTMLResponse)
async def get_index(request: Request):
    dix = dbm.get_date2units()
    return templates.TemplateResponse('index.html',
                                      {'request': request,
                                       'dix': dix})


@router.get('/lifting')
async def get_lifting(request: Request):
    dix = dbm.get_date2units()
    return templates.TemplateResponse('lifting.html', {'request': request})

    """
    {{ date.strftime('%d.%m.%y %H:%M:%S) }} <br>
    {% for s in sets %}
    {{ s.set_nr }} {{ s.weight }}Kg {{ s.reps }} {{ s.pause }}sec <br>
    {% endfor %}

"""