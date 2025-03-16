import uvicorn

# project imports
from .main import create_fastapi_app


def run_app():
    uvicorn.run('bushido:create_fastapi_app',
                port=8080,
                reload=True,
                factory=True,
                log_level='debug')

