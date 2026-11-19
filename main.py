from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from routes import routes

app = FastAPI()


app.add_middleware(
    CORSMiddleware,
    allow_origins=["https://your-portfolio.com", "http://localhost:5173"],
    allow_methods=["POST", "GET"],
    allow_headers=["Content-Type"],
)


@app.get("/health")
def health():
    return {"status": "ok"}


for route in routes:
    app.include_router(router=route.router, prefix=f"/api/v1/{route.name}")
