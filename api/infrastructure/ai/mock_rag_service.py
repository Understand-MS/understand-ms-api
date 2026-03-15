import json
from pathlib import Path

from api.domain.entities.conversation import Conversation
from api.domain.exceptions import RagServiceError
from api.infrastructure.ai.rag_service import RagService

MOCK_RESPONSES_DIR = Path(__file__).parent.parent.parent / "mock_responses"


class MockRagService(RagService):

    def __init__(self, response_type: str) -> None:
        self._response_type = response_type

    async def answer(self, question: str, conversation: Conversation) -> str:
        file_path = MOCK_RESPONSES_DIR / f"chat_{self._response_type}.json"
        payload = json.loads(file_path.read_text())

        if self._response_type == "error":
            raise RagServiceError(
                detail=payload["detail"],
                code=payload["code"],
            )

        return payload["answer"]