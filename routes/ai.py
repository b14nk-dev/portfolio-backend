from typing import Annotated

from fastapi import APIRouter
from fastapi.params import Body
from fastapi.responses import StreamingResponse

from schemas.ask_question import QuestionBody
from services.chat import start_new_chat

router = APIRouter()


@router.post("/")
def ai(body: Annotated[QuestionBody, Body()]):
    return StreamingResponse(
        start_new_chat(body.question),
        media_type="application/x-ndjson",
        headers={"X-Accel-Buffering": "no", "Cache-Control": "no-cache"},
    )
