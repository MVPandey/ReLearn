import pytest
from pydantic import ValidationError
from app.schema.llm.message import Message


def test_message_valid_data():
    """Test Message schema with valid data."""
    user_message = Message(role="user", content="Hello")
    assert user_message.role == "user"
    assert user_message.content == "Hello"

    assistant_message = Message(role="assistant", content="Hi there")
    assert assistant_message.role == "assistant"
    assert assistant_message.content == "Hi there"

    system_message = Message(role="system", content="You are a helpful assistant")
    assert system_message.role == "system"
    assert system_message.content == "You are a helpful assistant"


def test_message_invalid_role():
    """Test Message schema with invalid role."""
    with pytest.raises(ValidationError) as exc_info:
        Message(role="invalid_role", content="Hello")

    errors = exc_info.value.errors()
    assert any("role" in error["loc"] for error in errors)


def test_message_missing_fields():
    """Test Message schema with missing fields."""
    with pytest.raises(ValidationError):
        Message(content="Hello")

    with pytest.raises(ValidationError):
        Message(role="user")
