from fastapi import FastAPI

from api.routes import chat, health_check

app = FastAPI(
    title="Understand MS API",
    description="API for answering question about Multiple Sclerosis",
    version="1.0.0",
)

app.include_router(health_check.router)
app.include_router(chat.router)