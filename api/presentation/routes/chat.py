from typing import Annotated

from fastapi import APIRouter, Depends

from api.application.use_cases.ask_question import AskQuestionUseCase
from api.core.dependencies import get_ask_question_use_case
from api.presentation.models.chat_request import ChatRequest
from api.presentation.models.chat_response import ChatResponse

router = APIRouter(prefix="/chat", tags=["chat"])


@router.post("/", response_model=ChatResponse)
async def chat_endpoint(
    request: ChatRequest,
    use_case: Annotated[AskQuestionUseCase, Depends(get_ask_question_use_case)],
) -> ChatResponse:
    answer = await use_case.execute(question=request.question)
    return ChatResponse(answer=answer)