from collections import defaultdict
from fastapi import Request, APIRouter
from fastapi.templating import Jinja2Templates
from fastapi.responses import HTMLResponse
from babel.dates import format_date

# project imports
from bushido.utils.dt_functions import get_datetime_from_timestamp
from bushido.data.db_manager import DatabaseManager


# TODO investigate global variables
router = APIRouter()
templates = Jinja2Templates(directory='templates/')
templates.env.filters['format_datetime'] = format_date
templates.env.filters['timezone'] = get_datetime_from_timestamp


@router.get('/', response_class=HTMLResponse)
async def get_index(request: Request):
    dix = dbm.get_date2units()
    return templates.TemplateResponse('index.html',
                                      {'request': request,
                                       'dix': dix})


@router.get('/lifting')
async def get_lifting(request: Request):
    squats = dbm.cn2cat['lifting'].receive_all(unit_name='squat')
    dix = defaultdict(list)
    for squat in squats:
        dix[squat.timestamp].append(squat)

    deads = dbm.cn2cat['lifting'].receive_all(unit_name='deadlift')
    bench = dbm.cn2cat['lifting'].receive_all(unit_name='benchpress')
    ohp = dbm.cn2cat['lifting'].receive_all(unit_name='overheadpress')
    rows = dbm.cn2cat['lifting'].receive_all(unit_name='row')
    return templates.TemplateResponse('lifting.html',
                                      {'request': request,
                                       'squats': squats,
                                       'deads': deads,
                                       'bench': bench,
                                       'ohp': ohp,
                                       'rows': rows,
                                       })
