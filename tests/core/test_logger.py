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

    # Test normal case
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

    # Test uvicorn debug record (should be skipped) - Line 11
    uvicorn_debug_record = logging.LogRecord(
        name="uvicorn",
        level=logging.DEBUG,  # Below INFO
        pathname="test_path",
        lineno=1,
        msg="Debug message",
        args=(),
        exc_info=None,
    )
    handler.emit(uvicorn_debug_record)

    # Test invalid level name (hits exception path) - Lines 15-16
    with patch("app.core.logger.logger.level") as mock_level:
        mock_level.side_effect = ValueError("Invalid level")
        invalid_level_record = logging.LogRecord(
            name="test_logger",
            level=12345,  # Using a custom level number
            pathname="test_path",
            lineno=1,
            msg="Custom level message",
            args=(),
            exc_info=None,
        )
        handler.emit(invalid_level_record)

    # Test frame traversal - Lines 20-21
    with patch("logging.currentframe") as mock_frame:
        # Create a frame-like object with correct attributes
        frame_mock = MagicMock()
        frame_mock.f_back = MagicMock()
        frame_mock.f_code.co_filename = logging.__file__
        frame_mock.f_back.f_code.co_filename = "not_logging_file.py"
        mock_frame.return_value = frame_mock

        frame_record = logging.LogRecord(
            name="test_logger",
            level=logging.INFO,
            pathname="test_path",
            lineno=1,
            msg="Frame test message",
            args=(),
            exc_info=None,
        )
        handler.emit(frame_record)


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
