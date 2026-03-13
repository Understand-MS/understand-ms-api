from fastapi import APIRouter

from api.models.chat_request import ChatRequest
from api.models.chat_response import ChatResponse
from api.services.char_service import ask_question

router = APIRouter(
    prefix="/chat",
    tags=["chat"]
)

@router.post("/", response_model=ChatResponse)
async def chat_endpoint(request: ChatRequest) -> ChatResponse:
    answer = ask_question(request.question)
    return ChatResponse(answer=answer)