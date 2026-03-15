from abc import ABC, abstractmethod
from uuid import UUID

from api.domain.entities.conversation import Conversation


class ConversationRepository(ABC):

    @abstractmethod
    async def save(self, conversation: Conversation) -> Conversation:
        raise NotImplementedError

    @abstractmethod
    async def get_by_id(self, conversation_id: UUID) -> Conversation | None:
        raise NotImplementedError

    @abstractmethod
    async def list_all(self) -> list[Conversation]:
        raise NotImplementedError

    @abstractmethod
    async def delete(self, conversation_id: UUID) -> None:
        raise NotImplementedError