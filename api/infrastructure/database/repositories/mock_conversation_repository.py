from uuid import UUID

from api.domain.entities.conversation import Conversation
from api.domain.repositories.conversation_repository import ConversationRepository


class MockConversationRepository(ConversationRepository):

    def __init__(self) -> None:
        self._store: dict[UUID, Conversation] = {}

    async def save(self, conversation: Conversation) -> Conversation:
        self._store[conversation.id] = conversation
        return conversation

    async def get_by_id(self, conversation_id: UUID) -> Conversation | None:
        return self._store.get(conversation_id)

    async def list_all(self) -> list[Conversation]:
        return list(self._store.values())

    async def delete(self, conversation_id: UUID) -> None:
        self._store.pop(conversation_id, None)