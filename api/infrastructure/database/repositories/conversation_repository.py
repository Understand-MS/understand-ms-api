from uuid import UUID

from azure.cosmos.aio import ContainerProxy

from api.domain.entities.conversation import Conversation
from api.domain.repositories.conversation_repository import ConversationRepository


class CosmosConversationRepository(ConversationRepository):

    def __init__(self, container: ContainerProxy) -> None:
        self._container = container

    async def save(self, conversation: Conversation) -> Conversation:
        raise NotImplementedError

    async def get_by_id(self, conversation_id: UUID) -> Conversation | None:
        raise NotImplementedError

    async def list_all(self) -> list[Conversation]:
        raise NotImplementedError

    async def delete(self, conversation_id: UUID) -> None:
        raise NotImplementedError