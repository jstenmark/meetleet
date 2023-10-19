import os
from threading import Thread

import openai
from openai.error import RateLimitError

from src.config_manager import config
from src.constants import FILE_NAME_AUDIO, FILE_NAME_TRANSCRIPT, PATH
from src.prompts import (INTERVIEW_POSTION, LONGER_INSTRACT, SHORTER_INSTRACT,
                         SYSTEM_PROMPT)
from src.utils import logger, save_transcript_as_text

openai.api_key = config.OPENAI_API_KEY


def transcribe_audio(path_to_file) -> str:
    """
    Transcribes an audio file into text.

    Args:
        path_to_file (str, optional): The path to the audio file to be transcribed.

    Returns:
        str: The transcribed text.

    Raises:
        Exception: If the audio file fails to transcribe.
    """
    logger.debug(f"[TRANSCRIBE] INIT={path_to_file}")

    if os.path.getsize(path_to_file) == 0:
        logger.debug(f"[TRANSCRIPT] EMPTY_FILE={path_to_file}")
        return
    elif not os.path.exists(path_to_file):
        logger.debug(f"[TRANSCRIPT] NO_AUDIO={path_to_file}")
        return
    else:
        with open(path_to_file, "rb") as audio_file:
            try:
                logger.debug("[TRANSCRIBE] START WHISPER TRANSLATE")
                # https://github.com/openai/openai-cookbook/blob/main/examples/How_to_handle_rate_limits.ipynb
                transcript = openai.Audio.translate("whisper-1", audio_file)
                logger.debug("[TRANSCRIBE] FINISHED WHISPER TRANSLATE")
                # save_transcript_as_text(transcript["text"], FILE_NAME_TRANSCRIPT)
                # if transcript["text"] == "you":
                #     return "Whats best with python?"
                return transcript["text"]
            except RateLimitError as e:
                logger.exception(f"[TRANSCRIBE] RATELIMITED {e}")
                return "[TRANSCRIBE] RATELIMITED"
            except FileNotFoundError:
                logger.debug(f"[TRANSCRIBE] FILE={audio_file}")
                return f"[TRANSCRIBE] FILE={audio_file}"
            except Exception as error:
                logger.error(f"[TRANSCRIBE] ERROR={error}")
                return f"[TRANSCRIBE] ERROR={error}"


def generate_answer(
    transcript: str, short_answer: bool = True, temperature: float = 0.7
) -> str:
    """
    Generates an answer based on the given transcript using the OpenAI GPT-3.5-turbo model.

    Args:
        transcript (str): The transcript to generate an answer from.
        short_answer (bool): Whether to generate a short answer or not. Defaults to True.
        temperature (float): The temperature parameter for controlling the randomness of the generated answer.

    Returns:
        str: The generated answer.

    Example:
        ```python
        transcript = "Can you tell me about the weather?"
        answer = generate_answer(transcript, short_answer=False, temperature=0.8)
        print(answer)
        ```

    Raises:
        Exception: If the LLM fails to generate an answer.
    """
    if short_answer:
        system_prompt = SYSTEM_PROMPT + SHORTER_INSTRACT
    else:
        system_prompt = SYSTEM_PROMPT + LONGER_INSTRACT
    try:
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            temperature=temperature,
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": transcript},
            ],
        )
        logger.debug(f"[CHATGPT] SHORT={short_answer}")
        return response["choices"][0]["message"]["content"]
    except Exception as e:
        logger.error(f"[CHATGPT] ERROR={e}")
        return e
