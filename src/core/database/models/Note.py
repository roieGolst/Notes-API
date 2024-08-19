from datetime import datetime

from beanie import Document, PydanticObjectId
from pydantic import BaseModel
from pydantic import Field

class PostNoteRequest(BaseModel):
    title: str
    body: str

class PostNoteResponse(BaseModel):
    title: str
    body: str


class Note(Document):
    user_id: PydanticObjectId
    title: str
    body: str
    timestamps: datetime = Field(default_factory=datetime.now)
    sentiment: str

    class Settings:
        name = "notes"
