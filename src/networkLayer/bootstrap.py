from contextlib import asynccontextmanager

from fastapi import FastAPI

from src.database.init_db import init_db


@asynccontextmanager
async def lifespan(_: FastAPI):
    await init_db()
    yield
