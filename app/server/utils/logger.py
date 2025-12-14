import logging

from app.server.utils.config import get_config

LOG_LEVEL = get_config().log_level.upper()

def setup_logging() -> logging.Logger:
  """Configure structured logging for the API process."""
  return logging.getLogger("api")


logger = setup_logging()
