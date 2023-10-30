from datetime import datetime
from os.path import join
from threading import Thread

import numpy as np
import soundfile as sf
from loguru import logger

from src.config_manager import config


def generate_file_path(filename):
    return join(
        config.SRC_PATH + config.TMP_DIR,
        f"{datetime.now().strftime('%Y-%m-%d_%H:%M:%S.%f')}-{filename}",
    )


def save_transcript_to_audio(transcript, transcript_filename=config.FILE_NAME_TRANSCRIPT):
    def write_in_new_thread(filepath, transcript):
        try:
            with open(filepath, "w") as f:
                f.write(transcript)
                logger.debug(f"[TRANSCRIPT_SAVE] {filepath}")
        except Exception as e:
            logger.error(f"[TRANSCRIPT_SAVE] SAVE=False - Error: {e}")

    if transcript is None:
        logger.debug("[TRANSCRIPT_SAVE] SAVE=False - Empty transcript")
    else:
        Thread(
            target=write_in_new_thread,
            args=(generate_file_path(transcript_filename), transcript),
        ).start()


def save_audio_to_file(audio_data: np.ndarray, file_audio_path) -> None:
    """
    Saves an audio data array to a file.
    """
    try:
        if audio_data is None or not isinstance(audio_data, np.ndarray):
            logger.error("[AUDIO_SAVE] INVALID_CONTENT")
            return
        sf.write(file=file_audio_path, data=audio_data, samplerate=config.SAMPLE_RATE)
    except IOError:
        logger.error("[AUDIO_SAVE] WRITE FAILED")
    except Exception as e:
        logger.exception(f"[AUDIO_SAVE] ERRROR={e}")
