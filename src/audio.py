import numpy as np
import soundcard as sc
import soundfile as sf
import os

from src.utils import logger
from src.constants import FILE_NAME_LOG, LOG_LEVEL, RECORD_SEC, SAMPLE_RATE


SPEAKER_ID = str(sc.default_speaker().name)


def record_batch(record_sec: int = RECORD_SEC) -> np.ndarray:
    """
    Records an audio batch for a specified duration.

    Args:
        record_sec (int): The duration of the recording in seconds. Defaults to the value of RECORD_SEC.

    Returns:
        np.ndarray: The recorded audio sample.

    Example:
        ```python
        audio_sample = record_batch(5)
        ```
    """
    logger.debug(f"[AUDIO_RECORD] RECORDING={record_sec} seconds")
    with sc.get_microphone(
        id=SPEAKER_ID,
        include_loopback=True,
    ).recorder(samplerate=SAMPLE_RATE) as mic:
        audio_sample = mic.record(numframes=SAMPLE_RATE * record_sec)
        if audio_sample is None or not isinstance(audio_sample, np.ndarray):
            logger.error("[AUDIO_RECORD] INVALID_SAMPLE")
            return None
    return audio_sample


def save_audio_file(audio_data: np.ndarray, file_audio_path) -> None:
    """
    Saves an audio data array to a file.

    Args:
        audio_data (np.ndarray): The audio data to be saved.
        file_audio_path (str): The name of the output file.

    Returns:
        None

    Example:
        ```python
        audio_data = np.array([0.1, 0.2, 0.3])
        save_audio_file(audio_data, "output.wav")
        ```
    """
    try:
        if audio_data is None or not isinstance(audio_data, np.ndarray):
            logger.error("[AUDIO_SAVE] INVALID_CONTENT")
            return
        sf.write(file=file_audio_path, data=audio_data, samplerate=SAMPLE_RATE)
    except IOError:
        logger.error("[AUDIO_SAVE] WRITE FAILED")
    except Exception as e:
        logger.exception(f"[AUDIO_SAVE] ERRROR={e}")
