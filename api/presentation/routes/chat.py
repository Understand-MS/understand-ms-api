from typing import Annotated

from fastapi import APIRouter, Depends

from api.application.use_cases.ask_question import AskQuestionUseCase
from api.core.dependencies import get_ask_question_use_case
from api.presentation.models.chat_request import ChatRequest
from api.presentation.models.chat_response import ChatResponse
from api.presentation.models.message import Message

router = APIRouter(prefix="/chat", tags=["chat"])


@router.post("/", response_model=ChatResponse)
async def chat_endpoint(
    request: ChatRequest,
    use_case: Annotated[AskQuestionUseCase, Depends(get_ask_question_use_case)],
) -> ChatResponse:
    result = await use_case.execute(
        question=request.question,
        conversation_id=request.conversation_id,
    )
    return ChatResponse(
        id=result.conversation_id,
        answer=Message(
            id=result.message.id,
            role="assistant",
            content=result.message.answer,
            timestamp=result.message.created_at,
        ),
    )