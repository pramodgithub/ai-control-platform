# entry point for API

from fastapi import FastAPI
from app.api.routes import health, evaluate, replay, metrics


app = FastAPI(
    title="AI Control Platform",
    description="Structured AI Decision & Governance Engine",
    version="1.0.0"
)

app.include_router(health.router)
app.include_router(evaluate.router)
app.include_router(replay.router)
app.include_router(metrics.router)
