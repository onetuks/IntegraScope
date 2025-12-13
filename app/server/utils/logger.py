import logging

from app.server.utils.config import get_config

logger = logging.getLogger(__name__)

logger.setLevel(get_config().log_level)
