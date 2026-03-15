from api.domain.entities.conversation import Conversation


class RagService:

    async def answer(self, question: str, conversation: Conversation) -> str:
        raise NotImplementedError
