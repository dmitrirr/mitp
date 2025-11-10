from fastapi import FastAPI

from .routers.appeals import router

app = FastAPI()

app.include_router(router)

