from dataclasses import dataclass, field
from datetime import datetime
from uuid import UUID, uuid4


@dataclass
class Message:
    question: str
    answer: str
    created_at: datetime = field(default_factory=datetime.utcnow)


@dataclass
class Conversation:
    id: UUID = field(default_factory=uuid4)
    messages: list[Message] = field(default_factory=list)
    created_at: datetime = field(default_factory=datetime.utcnow)

    def add_message(self, question: str, answer: str) -> Message:
        message = Message(question=question, answer=answer)
        self.messages.append(message)
        return message
