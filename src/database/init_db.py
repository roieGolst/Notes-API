from beanie import init_beanie
import motor.motor_asyncio

from .models.User import User
from .models.Note import Note


async def init_db():
    client = motor.motor_asyncio.AsyncIOMotorClient(
        # # TODO: Replace with a configuration-based approach to improve testability.
        "mongodb://localhost:27017"
    )

    await init_beanie(database=client.notes_api, document_models=[User, Note])
