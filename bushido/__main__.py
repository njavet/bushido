import uvicorn

from bushido.core.conf import DEFAULT_PORT


def run_app():
    uvicorn.run('bushido.main:create_app',
                port=DEFAULT_PORT,
                reload=True,
                factory=True,
                log_level='debug')

run_app()
