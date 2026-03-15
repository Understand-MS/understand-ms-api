from collections.abc import AsyncGenerator
from typing import Annotated

from fastapi import Depends

from api.application.use_cases.ask_question import AskQuestionUseCase
from api.core.config import settings
from api.infrastructure.ai.mock_rag_service import MockRagService
from api.infrastructure.ai.rag_service import RagService
from api.infrastructure.database.connection import get_cosmos_client
from api.infrastructure.database.repositories.conversation_repository import (
    CosmosConversationRepository,
)
from api.infrastructure.database.repositories.mock_conversation_repository import (
    MockConversationRepository,
)


async def get_conversation_repository() -> AsyncGenerator[CosmosConversationRepository | MockConversationRepository, None]:
    if settings.is_mock_response:
        yield MockConversationRepository()
        return

    client = get_cosmos_client()
    async with client:
        container = client.get_database_client(settings.cosmos_database).get_container_client(
            settings.cosmos_conversations_container
        )
        yield CosmosConversationRepository(container)


async def get_rag_service() -> AsyncGenerator[RagService, None]:
    if settings.is_mock_response:
        yield MockRagService(response_type=settings.mock_response_type)
    else:
        yield RagService()


async def get_ask_question_use_case(
    repository: Annotated[CosmosConversationRepository, Depends(get_conversation_repository)],
    rag_service: Annotated[RagService, Depends(get_rag_service)],
) -> AsyncGenerator[AskQuestionUseCase, None]:
    yield AskQuestionUseCase(
        conversation_repository=repository,
        rag_service=rag_service,
    )