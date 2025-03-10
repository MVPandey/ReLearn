from fastapi.testclient import TestClient
from unittest.mock import patch

from app.main import app, logger, uvicorn

client = TestClient(app)


def test_health_check():
    """Test the health check endpoint returns the expected response."""
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json() == {"status": "healthy"}


def test_main_entry_point():
    """Test that the main entry point calls uvicorn.run with expected parameters."""
    with patch("uvicorn.run") as mock_run:
        uvicorn.run(
            app,
            host="0.0.0.0",
            port=8000,
            log_config=logger,
            log_level="info",
            access_log=True,
        )

        mock_run.assert_called_once()
        args, kwargs = mock_run.call_args
        assert args[0] == app
        assert kwargs["host"] == "0.0.0.0"
        assert kwargs["port"] == 8000
        assert kwargs["log_level"] == "info"
        assert kwargs["access_log"] is True
