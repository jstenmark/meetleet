import numpy as np
import soundcard as sc
from loguru import logger

from src.config_manager import config


def record_batch(record_sec: int = None) -> np.ndarray:
    record_sec = record_sec if record_sec is not None else config.RECORD_SEC
    logger.debug(f"[AUDIO_RECORD] RECORDING={record_sec} seconds")
    with sc.get_microphone(
        id=config.SPEAKER_ID,
        include_loopback=True,
    ).recorder(samplerate=config.SAMPLE_RATE) as mic:
        audio_sample = mic.record(numframes=config.SAMPLE_RATE * record_sec)
        if audio_sample is None or not isinstance(audio_sample, np.ndarray):
            logger.error("[AUDIO_RECORD] INVALID_SAMPLE")
            return None
    return audio_sample
