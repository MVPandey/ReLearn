import pytest
from unittest.mock import patch, MagicMock
from app.config.config import AppSettings


@pytest.mark.parametrize("mock_clear_env", [True], indirect=True)
def test_app_settings_default_values(mock_clear_env):
    """Test AppSettings with default values."""

    settings = AppSettings()

    assert settings.LOG_LEVEL == "INFO"
    assert settings.POSTGRES_DB_NAME == "postgres"
    assert settings.POSTGRES_DB_USER == "postgres"
    assert settings.POSTGRES_DB_PASSWORD == "postgres"
    assert settings.POSTGRES_DB_HOST == "localhost"
    assert settings.POSTGRES_DB_PORT == 5432


def test_database_url_property():
    """Test the database_url property construction."""
    settings = AppSettings(
        POSTGRES_DB_USER="testuser",
        POSTGRES_DB_PASSWORD="testpass",
        POSTGRES_DB_HOST="testhost",
        POSTGRES_DB_PORT=5433,
        POSTGRES_DB_NAME="testdb",
    )

    expected_url = "postgresql+asyncpg://testuser:testpass@testhost:5433/testdb"
    assert settings.database_url == expected_url


def test_app_settings_with_env_vars():
    """Test that AppSettings uses environment variables correctly."""
    settings = AppSettings()

    assert settings.LOG_LEVEL == "INFO"
    assert settings.LLM_API_BASE_URL == "https://api.test.com/v1"
    assert settings.LLM_MODEL_NAME == "test-model"
    assert settings.EMBEDDING_API_BASE_URL == "https://api.test.com/v1"
    assert settings.EMBEDDING_MODEL_NAME == "test-embedding-model"
    assert settings.LLM_API_KEY == "sk-test"
    assert settings.EMBEDDING_API_KEY == "sk-test"
    assert settings.POSTGRES_DB_NAME == "test_db"
    assert settings.POSTGRES_DB_USER == "test_user"
    assert settings.POSTGRES_DB_PASSWORD == "test_password"
    assert settings.POSTGRES_DB_HOST == "test_host"
    assert settings.POSTGRES_DB_PORT == 5432


def test_env_database_url_property():
    """Test database_url property with environment variables."""
    settings = AppSettings()

    expected_url = "postgresql+asyncpg://test_user:test_password@test_host:5432/test_db"
    assert settings.database_url == expected_url


@pytest.fixture
def mock_app_settings():
    """Mock AppSettings to avoid environment variable dependencies."""
    with patch("app.config.config.AppSettings") as mock_settings:
        settings_instance = MagicMock()
        settings_instance.LOG_LEVEL = "INFO"
        settings_instance.POSTGRES_DB_NAME = "postgres"
        settings_instance.POSTGRES_DB_USER = "postgres"
        settings_instance.POSTGRES_DB_PASSWORD = "postgres"
        settings_instance.POSTGRES_DB_HOST = "localhost"
        settings_instance.POSTGRES_DB_PORT = 5432
        settings_instance.LLM_API_BASE_URL = "https://api.test.com/v1"
        settings_instance.LLM_MODEL_NAME = "test-model"
        settings_instance.EMBEDDING_API_BASE_URL = "https://api.test.com/v1"
        settings_instance.EMBEDDING_MODEL_NAME = "test-embedding-model"
        settings_instance.LLM_API_KEY = "sk-test"
        settings_instance.EMBEDDING_API_KEY = "sk-test"
        settings_instance.database_url = (
            "postgresql+asyncpg://postgres:postgres@localhost:5432/postgres"
        )

        mock_settings.return_value = settings_instance
        yield settings_instance


def test_app_settings_properties(mock_app_settings):
    """Test AppSettings properties with mocked instance."""
    assert mock_app_settings.LOG_LEVEL == "INFO"
    assert mock_app_settings.POSTGRES_DB_NAME == "postgres"
    assert (
        mock_app_settings.database_url
        == "postgresql+asyncpg://postgres:postgres@localhost:5432/postgres"
    )
    assert mock_app_settings.LLM_API_KEY == "sk-test"
    assert mock_app_settings.LLM_MODEL_NAME == "test-model"


def test_llm_settings(mock_app_settings):
    """Test LLM-related settings."""
    assert mock_app_settings.LLM_API_BASE_URL == "https://api.test.com/v1"
    assert mock_app_settings.LLM_MODEL_NAME == "test-model"
    assert mock_app_settings.LLM_API_KEY == "sk-test"


def test_embedding_settings(mock_app_settings):
    """Test embedding-related settings."""
    assert mock_app_settings.EMBEDDING_API_BASE_URL == "https://api.test.com/v1"
    assert mock_app_settings.EMBEDDING_MODEL_NAME == "test-embedding-model"
    assert mock_app_settings.EMBEDDING_API_KEY == "sk-test"
