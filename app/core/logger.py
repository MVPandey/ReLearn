from loguru import logger
import sys
import logging

from config.config import app_settings


class InterceptHandler(logging.Handler):
    def emit(self, record):
        if record.name == "uvicorn" and record.levelno < logging.INFO:
            return

        try:
            level = logger.level(record.levelname).name
        except ValueError:
            level = record.levelno

        frame, depth = logging.currentframe(), 2
        while frame and frame.f_code.co_filename == logging.__file__:
            frame = frame.f_back
            depth += 1

        logger.opt(depth=depth, exception=record.exc_info).log(
            level, record.getMessage()
        )


logger.remove()

logger.add(
    sys.stderr,
    level=app_settings.LOG_LEVEL or "INFO",
    format="<green>{time:YYYY-MM-DD HH:mm:ss}</green> | <level>{level: <8}</level> | <cyan>{name}</cyan>:<cyan>{function}</cyan>:<cyan>{line}</cyan> - <level>{message}</level>",
)

logger.add(
    "logs/app.log",
    rotation="00:00",
    retention="3 days",
    level=app_settings.LOG_LEVEL or "INFO",
    format="{time:YYYY-MM-DD HH:mm:ss} | {level: <8} | {name}:{function}:{line} - {message}",
    compression="zip",
    backtrace=True,
    diagnose=True,
    enqueue=True,
)

for logger_name in ["uvicorn", "uvicorn.error", "uvicorn.access", "fastapi"]:
    logging.getLogger(logger_name).setLevel(logging.INFO)

logging.basicConfig(handlers=[InterceptHandler()], level=logging.INFO, force=True)

for _log in ["uvicorn", "uvicorn.error", "uvicorn.access", "fastapi"]:
    _logger = logging.getLogger(_log)
    _logger.handlers = [InterceptHandler()]
    _logger.propagate = False

logging.getLogger("logging").setLevel(logging.WARNING)

__all__ = ["logger"]
