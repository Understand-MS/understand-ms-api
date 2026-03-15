from uuid import UUID

import pytest

from api.domain.entities.conversation import Conversation, Message


def test_conversation_has_unique_id():
    c1 = Conversation()
    c2 = Conversation()
    assert c1.id != c2.id


def test_conversation_id_is_uuid():
    conversation = Conversation()
    assert isinstance(conversation.id, UUID)


def test_conversation_starts_with_no_messages():
    conversation = Conversation()
    assert conversation.messages == []


def test_add_message_returns_message():
    conversation = Conversation()
    message = conversation.add_message(question="What is MS?", answer="MS is...")
    assert isinstance(message, Message)


def test_add_message_appended_to_conversation():
    conversation = Conversation()
    conversation.add_message(question="What is MS?", answer="MS is...")
    assert len(conversation.messages) == 1


def test_add_message_stores_question_and_answer():
    conversation = Conversation()
    conversation.add_message(question="What is MS?", answer="MS is a disease.")
    message = conversation.messages[0]
    assert message.question == "What is MS?"
    assert message.answer == "MS is a disease."


def test_add_multiple_messages_preserves_order():
    conversation = Conversation()
    conversation.add_message(question="Q1", answer="A1")
    conversation.add_message(question="Q2", answer="A2")
    assert conversation.messages[0].question == "Q1"
    assert conversation.messages[1].question == "Q2"


def test_message_has_created_at():
    conversation = Conversation()
    message = conversation.add_message(question="Q", answer="A")
    assert message.created_at is not None


def test_conversation_has_created_at():
    conversation = Conversation()
    assert conversation.created_at is not None
