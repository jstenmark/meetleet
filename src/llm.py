import os

import openai
from loguru import logger
from openai.error import RateLimitError

from src.config_manager import config
from src.utils import save_transcript_to_audio

openai.api_key = config.OPENAI_API_KEY


def transcribe_audio(path_to_file) -> str:
    """
    Transcribes an audio file into text.
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

                save_transcript_to_audio(transcript["text"], config.FILE_NAME_TRANSCRIPT)
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
    transcript: str,
    short_answer: bool = True,
    temperature: float = 0.7,
    max_tokens=None,
) -> str:
    """
    Generates an answer based on the given transcript using the OpenAI GPT-3.5-turbo model.
    """
    if short_answer:
        system_prompt = config.SYSTEM_PROMPT + config.SHORTER_INSTRUCT
        max_tokens = 140
    else:
        system_prompt = config.SYSTEM_PROMPT + config.LONGER_INSTRUCT
        max_tokens = 300
    try:
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            temperature=temperature,
            max_tokens=max_tokens,
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


def num_tokens_from_messages(messages, model="gpt-3.5-turbo"):
    """Returns the number of tokens used by a list of messages."""
    import tiktoken

    try:
        encoding = tiktoken.encoding_for_model(model)
    except ValueError:
        print("Warning: model not found. Using cl100k_base encoding.")
        encoding = tiktoken.get_encoding("cl100k_base")

    if model[:7] == "gpt-3.5":
        tokens_per_message = 4  # every message follows <|start|>{role/name}\n{content}<|end|>\n
        tokens_per_name = -1  # if there's a name, the role is omitted
    elif model[:5] == "gpt-4":
        tokens_per_message = 3
        tokens_per_name = 1
    else:
        raise NotImplementedError(
            f"""num_tokens_from_messages() is not implemented for model {model}. See https://github.com/openai/openai-python/blob/main/chatml.md for information on how messages are converted to tokens."""
        )
    num_tokens = 0
    for message in messages:
        num_tokens += tokens_per_message
        for key, value in message.items():
            num_tokens += len(encoding.encode(value))
            if key == "name":
                num_tokens += tokens_per_name
    num_tokens += 3  # every reply is primed with <|start|>assistant<|message|>
    return num_tokens
