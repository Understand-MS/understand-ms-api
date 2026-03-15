from uuid import UUID

from api.domain.entities.conversation import Conversation
from api.domain.repositories.conversation_repository import ConversationRepository
from api.infrastructure.ai.rag_service import RagService


class AskQuestionUseCase:

    def __init__(
        self,
        conversation_repository: ConversationRepository,
        rag_service: RagService,
    ) -> None:
        self._conversation_repository = conversation_repository
        self._rag_service = rag_service

    async def execute(self, question: str, conversation_id: UUID | None = None) -> str:
        if conversation_id:
            conversation = await self._conversation_repository.get_by_id(conversation_id)
        else:
            conversation = None

        if conversation is None:
            conversation = Conversation()

        answer = await self._rag_service.answer(question, conversation)

        conversation.add_message(question=question, answer=answer)
        await self._conversation_repository.save(conversation)

        return answer
