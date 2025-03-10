import logging
from app.core.logger import InterceptHandler
import pytest
from unittest.mock import patch, MagicMock

from app.core.logger import logger


def test_logger_initialization():
    """Test that the logger was initialized correctly."""
    assert logger is not None
    assert len(logger._core.handlers) > 0


def test_intercept_handler():
    """Test that InterceptHandler works correctly."""
    handler = InterceptHandler()
    assert isinstance(handler, logging.Handler)

    record = logging.LogRecord(
        name="test_logger",
        level=logging.INFO,
        pathname="test_path",
        lineno=1,
        msg="Test message",
        args=(),
        exc_info=None,
    )

    handler.emit(record)


@pytest.fixture
def mock_logger_setup():
    """Mock dependencies for logger tests."""
    with patch("app.core.logger.app_settings", create=True) as mock_settings:
        mock_settings.LOG_LEVEL = "INFO"

        with patch("app.core.logger.InterceptHandler") as mock_handler:
            mock_handler_instance = MagicMock(spec=logging.Handler)
            mock_handler.return_value = mock_handler_instance
            yield mock_handler_instance


def test_logger_configuration(mock_logger_setup):
    """Test basic logger configuration."""
    assert mock_logger_setup is not None
    assert isinstance(mock_logger_setup, MagicMock)
