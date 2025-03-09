import uvicorn
from pathlib import Path
from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse, HTMLResponse
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles

# project imports


def create_fastapi_app():
    app = FastAPI()
    app.mount('/static', StaticFiles(directory='static'), name='static')
    templates = Jinja2Templates(directory='templates')

    @app.get('/', response_class=HTMLResponse)
    async def index(request: Request):
        return templates.TemplateResponse('index.html',
                                          {'request': request})

    return app
