import pytest
import os
from unittest.mock import AsyncMock, patch
from openai import AsyncOpenAI
from openai.types.chat.chat_completion import (
    ChatCompletion,
    Choice,
    ChatCompletionMessage,
)
from app.services.llm_service import LLMService
from app.schema.llm.message import Message
from app.core.exceptions import LLMException


@pytest.fixture
def llm_service():
    """Create an LLM service for testing."""
    return LLMService(
        base_url=os.environ.get("LLM_API_BASE_URL"),
        api_key=os.environ.get("LLM_API_KEY"),
        model_name=os.environ.get("LLM_MODEL_NAME"),
    )


def test__client_initialization(llm_service):
    assert isinstance(llm_service._client(), AsyncOpenAI)


@pytest.mark.asyncio
async def test_query_llm_success(llm_service):
    """Test successful LLM query with a single message."""
    message = Message(role="user", content="Hello")
    mock_response = ChatCompletion(
        id="123",
        choices=[
            Choice(
                index=0,
                message=ChatCompletionMessage(role="assistant", content="Hi there"),
                finish_reason="stop",
            )
        ],
        created=1234567890,
        model="test-model",
        object="chat.completion",
    )

    with patch.object(llm_service, "_client") as mock_client:
        mock_client.return_value.chat.completions.create = AsyncMock(
            return_value=mock_response
        )

        response = await llm_service.query_llm(message)

        assert response.role == "assistant"
        assert response.content == "Hi there"
        mock_client.return_value.chat.completions.create.assert_called_once()


@pytest.mark.asyncio
async def test_query_llm_with_json_response(llm_service):
    """Test LLM query with JSON response format."""
    message = Message(role="user", content="Hello")
    json_content = '{"greeting": "Hello", "response": "Hi there"}'
    mock_response = ChatCompletion(
        id="123",
        choices=[
            Choice(
                index=0,
                message=ChatCompletionMessage(role="assistant", content=json_content),
                finish_reason="stop",
            )
        ],
        created=1234567890,
        model="test-model",
        object="chat.completion",
    )

    with patch.object(llm_service, "_client") as mock_client:
        mock_client.return_value.chat.completions.create = AsyncMock(
            return_value=mock_response
        )

        response = await llm_service.query_llm(message, json_response=True)

        assert isinstance(response, dict)
        assert response["greeting"] == "Hello"
        assert response["response"] == "Hi there"
        mock_client.return_value.chat.completions.create.assert_called_once()


@pytest.mark.asyncio
async def test_query_llm_with_json_decode_error(llm_service):
    """Test LLM query with invalid JSON response."""
    message = Message(role="user", content="Hello")
    invalid_json = "{invalid json}"
    mock_response = ChatCompletion(
        id="123",
        choices=[
            Choice(
                index=0,
                message=ChatCompletionMessage(role="assistant", content=invalid_json),
                finish_reason="stop",
            )
        ],
        created=1234567890,
        model="test-model",
        object="chat.completion",
    )

    with patch.object(llm_service, "_client") as mock_client:
        mock_client.return_value.chat.completions.create = AsyncMock(
            return_value=mock_response
        )

        with pytest.raises(LLMException) as exc_info:
            await llm_service.query_llm(message, json_response=True)

        assert "Failed to parse JSON response" in str(exc_info.value)


@pytest.mark.asyncio
async def test_query_llm_with_generic_exception(llm_service):
    """Test LLM query with a generic exception."""
    message = Message(role="user", content="Hello")

    with patch.object(llm_service, "_client") as mock_client:
        mock_client.return_value.chat.completions.create = AsyncMock(
            side_effect=Exception("Test exception")
        )

        with pytest.raises(LLMException) as exc_info:
            await llm_service.query_llm(message)

        assert isinstance(exc_info.value, LLMException)
        assert "Failed to query LLM" in str(exc_info.value)
