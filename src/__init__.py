
from loguru import logger

from src.config_manager import config

for key, value in config.__dict__.items():
    globals()[key] = value

logger.add(config.SRC_PATH + config.FILE_NAME_LOG, level=config.LOG_LEVEL, rotation="5 MB", enqueue=True)


