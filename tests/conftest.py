import pytest
import os
from unittest.mock import patch

os.environ.update(
    {
        "LOG_LEVEL": "INFO",
        "LLM_API_BASE_URL": "https://api.test.com/v1",
        "LLM_MODEL_NAME": "test-model",
        "EMBEDDING_API_BASE_URL": "https://api.test.com/v1",
        "EMBEDDING_MODEL_NAME": "test-embedding-model",
        "LLM_API_KEY": "sk-test",
        "EMBEDDING_API_KEY": "sk-test",
        "POSTGRES_DB_NAME": "test_db",
        "POSTGRES_DB_USER": "test_user",
        "POSTGRES_DB_PASSWORD": "test_password",
        "POSTGRES_DB_HOST": "test_host",
        "POSTGRES_DB_PORT": "5432",
    }
)


@pytest.fixture(scope="session", autouse=True)
def ensure_test_environment():
    """Ensure we're running in a test environment."""
    assert (
        os.environ.get("LLM_API_KEY") == "sk-test"
    ), "Test environment not properly configured"
    yield


@pytest.fixture(autouse=True)
def mock_env_vars():
    """Provide mock environment variables for tests."""
    env_vars = {
        "LOG_LEVEL": "INFO",
        "LLM_API_BASE_URL": "https://api.test.com/v1",
        "LLM_MODEL_NAME": "test-model",
        "EMBEDDING_API_BASE_URL": "https://api.test.com/v1",
        "EMBEDDING_MODEL_NAME": "test-embedding-model",
        "LLM_API_KEY": "sk-test",
        "EMBEDDING_API_KEY": "sk-test",
        "POSTGRES_DB_NAME": "test_db",
        "POSTGRES_DB_USER": "test_user",
        "POSTGRES_DB_PASSWORD": "test_password",
        "POSTGRES_DB_HOST": "test_host",
        "POSTGRES_DB_PORT": "5432",
    }

    with patch.dict(os.environ, env_vars):
        yield


@pytest.fixture
def mock_clear_env(request):
    """Fixture to clear environment variables for default settings tests."""
    original_environ = os.environ.copy()

    if request.param:
        os.environ.clear()

    yield

    os.environ.clear()
    os.environ.update(original_environ)
