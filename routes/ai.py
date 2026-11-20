from fastapi import APIRouter, Request
from fastapi.responses import StreamingResponse

from schemas.ask_question import QuestionBody
from services.chat import start_new_chat
from utils.client_rate_limit import LIMIT, limiter

router = APIRouter()


@router.get("/warmup")
def warmup():
    return {"status": "ready"}


@router.post("/")
@limiter.limit(LIMIT)
def ai(request: Request, body: QuestionBody):
    return StreamingResponse(
        start_new_chat(body.question),
        media_type="application/x-ndjson",
        headers={"X-Accel-Buffering": "no", "Cache-Control": "no-cache"},
    )
