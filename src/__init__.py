import sys


def get_config():
    global config
    from src.config_manager import ConfigManager
    config = ConfigManager()
    return config

def get_logger():
    global logger
    from loguru import logger
    config = get_config()
    logger.add(config.SRC_PATH + config.FILE_NAME_LOG, level=config.LOG_LEVEL, rotation="10 MB", enqueue=True)
    logger.add(sys.stdout, level=config.LOG_LEVEL, enqueue=True)
    return logger


config = get_config()

logger = get_logger()