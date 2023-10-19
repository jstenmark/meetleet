import os
from pathlib import Path

from dotenv import load_dotenv


class ConfigManager:
    def __init__(self):

        env_path = os.path.join(os.path.dirname(__file__), '../.env')
        load_dotenv(dotenv_path=env_path)

        self.OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
        self.LOG_LEVEL = os.getenv("LOG_LEVEL", "DEBUG")
        self.FILE_NAME_LOG = os.getenv("FILE_NAME_LOG")
        self.FILE_NAME_TRANSCRIPT = os.getenv("FILE_NAME_TRANSCRIPT")
        self.FILE_NAME_AUDIO = os.getenv("FILE_NAME_AUDIO")
        self.SRC_PATH = os.getenv("SRC_PATH")


        self.INTERVIEW_POSITION = os.getenv("INTERVIEW_POSITION")
        self.SYSTEM_PROMPT = os.getenv("SYSTEM_PROMPT").format(INTERVIEW_POSITION=os.getenv("INTERVIEW_POSITION"))
        self.SHORTER_INSTRUCT = os.getenv("SHORTER_INSTRUCT")
        self.LONGER_INSTRUCT = os.getenv("LONGER_INSTRUCT")

        self.SAMPLE_RATE = 48000  # [Hz]. sampling rate.
        self.RECORD_SEC = 1  # [sec]. duration recording audio.


    def echo_config(self):
        for key, value in self.__dict__.items():
            print(f"{key}: {value}")


_config = ConfigManager()
