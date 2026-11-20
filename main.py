from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from slowapi.errors import RateLimitExceeded

from routes.ai import router as ai_router
from utils.client_rate_limit import limiter, rate_limit_exceeded_handler

app = FastAPI()
app.state.limiter = limiter
app.add_exception_handler(RateLimitExceeded, rate_limit_exceeded_handler)


app.add_middleware(
    CORSMiddleware,
    allow_origins=["https://ritik-negi.vercel.app"],
    allow_origin_regex=r"http://(localhost|127\.0\.0\.1)(:\d+)?",
    allow_methods=["POST", "GET"],
    allow_headers=["Content-Type"],
    expose_headers=["Retry-After"],
)


@app.get("/health")
def health():
    return {"status": "ok"}


app.include_router(ai_router, prefix="/api/v1/ai")
