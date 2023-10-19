import importlib
import sys

from loguru import logger as loguru_logger


def get_config():
    from src.config_manager import ConfigManager
    conf = ConfigManager()
    return conf

loguru_logger.add(get_config().SRC_PATH + get_config().FILE_NAME_LOG, level=get_config().LOG_LEVEL, rotation="10 MB", enqueue=True)
loguru_logger.add(sys.stdout, level=get_config().LOG_LEVEL, enqueue=True)
logger = loguru_logger

