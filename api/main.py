from fastapi import FastAPI
from fastapi.responses import JSONResponse

from api.core.config import settings
from api.domain.exceptions import RagServiceError
from api.presentation.routes import chat, health_check

app = FastAPI(
    title=settings.app_name,
    description="API for answering questions about Multiple Sclerosis",
    version=settings.app_version,
)

app.include_router(health_check.router)
app.include_router(chat.router)


@app.exception_handler(RagServiceError)
async def rag_service_error_handler(request, exc: RagServiceError) -> JSONResponse:
    return JSONResponse(
        status_code=503,
        content={"detail": exc.detail, "code": exc.code},
    )