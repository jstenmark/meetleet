import sys
from datetime import datetime
from os.path import join

import PySimpleGUI as sg

from src import get_config, logger

config = get_config()


def generate_audio_path():
    return join(
        config.SRC_PATH, f"{datetime.now().strftime('%Y-%m-%d_%H:%M:%S.%f')}-{config.FILE_NAME_AUDIO}"
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
