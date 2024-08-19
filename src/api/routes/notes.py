from fastapi import APIRouter

from ..middlewares.authenticate import AuthDep, AuthAndGetSingDep
from src.core.database.models.Note import Note
from src.services.sentiment.SentimentService import analyze_sentiment
from src.core.database.models.Note import PostNoteRequest

router = APIRouter(prefix="/notes")


@router.post(
    path="/",
    dependencies=[AuthDep]
)
async def create_new_note(note: PostNoteRequest,  token: AuthAndGetSingDep):
    sentiment = analyze_sentiment(note.body)

    new_note = Note(
        user_id=token['id'],
        title=note.title,
        body=note.body,
        sentiment=sentiment.__str__()
    )

    await new_note.insert()
