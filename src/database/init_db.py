from beanie import init_beanie
import motor.motor_asyncio

from .models.User import User


async def init_db():
    client = motor.motor_asyncio.AsyncIOMotorClient(
        "mongodb://localhost:27017"
    )

    await init_beanie(database=client.notes_api, document_models=[User])
