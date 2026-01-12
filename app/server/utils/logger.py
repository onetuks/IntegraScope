import logging

from app.server.utils.config import get_config

LOG_LEVEL = get_config().log_level.upper()


def setup_logging() -> logging.Logger:
    """Configure structured logging for the API process."""
    logger_ = logging.getLogger("api")
    logger_.setLevel(LOG_LEVEL)
    return logger_


logger = setup_logging()
