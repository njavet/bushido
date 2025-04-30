from fastapi import Request, APIRouter, HTTPException


router = APIRouter()


@router.get('/api/wimhof-units')
async def get_wimhof_units(request: Request):
    service = request.state.bot.unit_service['wimhof']
    pass
