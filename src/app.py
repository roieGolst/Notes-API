from fastapi import FastAPI

from src.api.routes.auth import router as auth_router
from src.api.routes.notes import router as notes_router
from src.api.bootstrap import lifespan

app = FastAPI(lifespan=lifespan)

app.include_router(
    router=auth_router,
    tags=["Auth"]
)

app.include_router(
    router=notes_router,
    tags=["Notes"]
)