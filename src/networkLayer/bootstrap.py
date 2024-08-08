from contextlib import asynccontextmanager
from os.path import dirname, join

from dotenv import load_dotenv
from fastapi import FastAPI

from src.database.init_db import init_db

ENV_PATH = join(dirname(__file__), "..", "..", "configs", ".env")


@asynccontextmanager
async def lifespan(_: FastAPI):
    load_dotenv(ENV_PATH)
    await init_db()
    yield
