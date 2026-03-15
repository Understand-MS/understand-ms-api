from unittest.mock import AsyncMock
from uuid import uuid4

import pytest

from api.application.use_cases.ask_question import AskQuestionUseCase
from api.domain.entities.conversation import Conversation


@pytest.fixture
def mock_repository():
    repo = AsyncMock()
    repo.get_by_id.return_value = None
    repo.save.side_effect = lambda conversation: conversation
    return repo


@pytest.fixture
def mock_rag_service():
    rag = AsyncMock()
    rag.answer.return_value = "MS is a chronic autoimmune disease."
    return rag


@pytest.fixture
def use_case(mock_repository, mock_rag_service):
    return AskQuestionUseCase(
        conversation_repository=mock_repository,
        rag_service=mock_rag_service,
    )


async def test_returns_answer_from_rag_service(use_case, mock_rag_service):
    answer = await use_case.execute(question="What is MS?")
    assert answer == "MS is a chronic autoimmune disease."


async def test_creates_new_conversation_when_no_id_given(use_case, mock_repository):
    await use_case.execute(question="What is MS?")
    mock_repository.get_by_id.assert_not_called()


async def test_saves_conversation_after_answering(use_case, mock_repository):
    await use_case.execute(question="What is MS?")
    mock_repository.save.assert_called_once()


async def test_saved_conversation_contains_message(use_case, mock_repository):
    await use_case.execute(question="What is MS?")
    saved_conversation: Conversation = mock_repository.save.call_args[0][0]
    assert len(saved_conversation.messages) == 1
    assert saved_conversation.messages[0].question == "What is MS?"
    assert saved_conversation.messages[0].answer == "MS is a chronic autoimmune disease."


async def test_loads_existing_conversation_when_id_given(use_case, mock_repository):
    existing = Conversation()
    mock_repository.get_by_id.return_value = existing
    conversation_id = existing.id

    await use_case.execute(question="What is MS?", conversation_id=conversation_id)

    mock_repository.get_by_id.assert_called_once_with(conversation_id)


async def test_appends_to_existing_conversation(use_case, mock_repository):
    existing = Conversation()
    existing.add_message(question="Previous Q", answer="Previous A")
    mock_repository.get_by_id.return_value = existing

    await use_case.execute(question="New Q", conversation_id=existing.id)

    saved_conversation: Conversation = mock_repository.save.call_args[0][0]
    assert len(saved_conversation.messages) == 2


async def test_creates_new_conversation_when_id_not_found(use_case, mock_repository):
    mock_repository.get_by_id.return_value = None
    unknown_id = uuid4()

    await use_case.execute(question="What is MS?", conversation_id=unknown_id)

    saved_conversation: Conversation = mock_repository.save.call_args[0][0]
    assert len(saved_conversation.messages) == 1


async def test_passes_conversation_context_to_rag(use_case, mock_repository, mock_rag_service):
    existing = Conversation()
    mock_repository.get_by_id.return_value = existing

    await use_case.execute(question="Follow-up question", conversation_id=existing.id)

    call_args = mock_rag_service.answer.call_args
    assert call_args[0][0] == "Follow-up question"
    assert call_args[0][1] is existing