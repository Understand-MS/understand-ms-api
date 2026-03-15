from uuid import UUID

from pydantic import BaseModel

from api.presentation.models.message import Message


class ChatResponse(BaseModel):
    id: UUID
    answer: Message