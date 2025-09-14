from fastapi import FastAPI
from starlette.middleware.cors import CORSMiddleware

# project imports
from bushido.web import router


def create_app():
    app = FastAPI()

    app.add_middleware(CORSMiddleware,
                       allow_origins=['http://localhost:5173'],
                       allow_methods=["*"],
                       allow_headers=["*"],)
    app.include_router(router)
    return app
