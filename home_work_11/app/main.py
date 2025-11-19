from fastapi import FastAPI

from .dependencies import _engine
from .routers.auth import router as auth_router
from .routers.students import router
from app.db.models import Base

app = FastAPI()


@app.on_event("startup")
def create_tables():
    Base.metadata.create_all(bind=_engine)


app.include_router(router)
app.include_router(auth_router)
