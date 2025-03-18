from fastapi import FastAPI

from src.app.routes import api

app = FastAPI()

app.include_router(api.router)
