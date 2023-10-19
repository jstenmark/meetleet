import sys
from datetime import datetime
from os.path import join

import PySimpleGUI as sg
from loguru import logger

from src.config_manager import config
from src.constants import FILE_NAME_AUDIO, FILE_NAME_LOG, OFF_IMAGE, SRC_PATH

logger.add(SRC_PATH + FILE_NAME_LOG, level=config.LOG_LEVEL, rotation="10 MB", enqueue=True)
logger.add(sys.stdout, level=config.LOG_LEVEL, enqueue=True)

def generate_audio_path():
    return join(
        SRC_PATH, f"{datetime.now().strftime('%Y-%m-%d_%H:%M:%S.%f')}-{FILE_NAME_AUDIO}"
    )


def save_transcript_as_text(transcript, transcript_filename):
    if transcript is not None:
        logger.debug(f"[TRANSCRIPT] {transcript}")
        try:
            with open(transcript_filename, "w") as f:
                f.write(transcript)
        except Exception as e:
            logger.error(f"[TRANSCRIPT] SAVE=False, Error: {e}")
    else:
        logger.debug("[TRANSCRIPT] Empty transcript, couldn't save")
