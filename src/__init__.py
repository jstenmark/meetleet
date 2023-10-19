import sys

from loguru import logger

from src.config_manager import config

logger.add(config.SRC_PATH + config.FILE_NAME_LOG, level=config.LOG_LEVEL, rotation="10 MB", enqueue=True)
logger.add(sys.stdout, level=config.LOG_LEVEL, enqueue=True)
