from datetime import datetime
from typing import Literal
from uuid import UUID

from pydantic import BaseModel


class Message(BaseModel):
    id: UUID
    role: Literal["user", "assistant"]
    content: str
    timestamp: datetime