from datetime import datetime

from beanie import Document, PydanticObjectId
from pydantic import Field


class Note(Document):
    user_id: PydanticObjectId
    title: str
    body: str
    timestamps: datetime = Field(default_factory=datetime.now)
    sentiment: str

    class Config:
        name = "notes"
