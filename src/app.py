from fastapi import FastAPI

from src.networkLayer.routes.auth import router as router
from src.networkLayer.bootstrap import lifespan

app = FastAPI(lifespan=lifespan)
app.include_router(router)


@app.get("/")
async def index() -> dict:
    return {"message": "Welcome to your books app!"}
