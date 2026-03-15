from datetime import datetime
from uuid import UUID

from azure.cosmos.aio import ContainerProxy
from azure.cosmos.exceptions import CosmosResourceNotFoundError

from api.domain.entities.conversation import Conversation, Message
from api.domain.repositories.conversation_repository import ConversationRepository


class CosmosConversationRepository(ConversationRepository):

    def __init__(self, container: ContainerProxy) -> None:
        self._container = container

    async def save(self, conversation: Conversation) -> Conversation:
        document = self._to_document(conversation)
        await self._container.upsert_item(document)
        return conversation

    async def get_by_id(self, conversation_id: UUID) -> Conversation | None:
        try:
            document = await self._container.read_item(
                item=str(conversation_id),
                partition_key=str(conversation_id),
            )
            return self._from_document(document)
        except CosmosResourceNotFoundError:
            return None

    async def list_all(self) -> list[Conversation]:
        raise NotImplementedError

    async def delete(self, conversation_id: UUID) -> None:
        raise NotImplementedError

    def _to_document(self, conversation: Conversation) -> dict:
        return {
            "id": str(conversation.id),
            "created_at": conversation.created_at.isoformat(),
            "messages": [
                {
                    "id": str(message.id),
                    "question": message.question,
                    "answer": message.answer,
                    "created_at": message.created_at.isoformat(),
                }
                for message in conversation.messages
            ],
        }

    def _from_document(self, document: dict) -> Conversation:
        conversation = Conversation(id=UUID(document["id"]))
        conversation.created_at = datetime.fromisoformat(document["created_at"])
        conversation.messages = [
            Message(
                id=UUID(msg["id"]),
                question=msg["question"],
                answer=msg["answer"],
                created_at=datetime.fromisoformat(msg["created_at"]),
            )
            for msg in document.get("messages", [])
        ]
        return conversation