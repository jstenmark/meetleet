from os import getenv
from pathlib import Path

from dotenv import load_dotenv

from assets.constants import OFF_IMAGE, ON_IMAGE


class ConfigManager:
    def __init__(self):
        FILE_PATH_DOTENV = Path(__file__).resolve().parent / f"../{getenv('FILE_DOTENV', '.env')}"

        print(f"DOTENV PATH={FILE_PATH_DOTENV}")

        load_dotenv(dotenv_path=FILE_PATH_DOTENV)

        # API
        self.OPENAI_API_KEY = getenv("OPENAI_API_KEY")

        # Log Settings
        self.LOG_LEVEL = getenv("LOG_LEVEL", "DEBUG")
        self.PRINT_CONFIG = getenv("PRINT_CONFIG", False)

        # Paths/Files
        self.SRC_PATH = getenv("SRC_PATH")
        self.FILE_NAME_LOG = getenv("FILE_NAME_LOG")
        self.FILE_NAME_AUDIO = getenv("FILE_NAME_AUDIO")
        self.FILE_NAME_TRANSCRIPT = getenv("FILE_NAME_TRANSCRIPT")

        # Prompt
        self.INTERVIEW_POSITION = getenv("INTERVIEW_POSITION")
        self.SYSTEM_PROMPT = getenv("SYSTEM_PROMPT").format(INTERVIEW_POSITION=getenv("INTERVIEW_POSITION"))
        self.SHORTER_INSTRUCT = getenv("SHORTER_INSTRUCT")
        self.LONGER_INSTRUCT = getenv("LONGER_INSTRUCT")

        # Audio
        self.SAMPLE_RATE = 48000  # [Hz]. sampling rate.
        self.RECORD_SEC = 1  # [sec]. duration recording audio.

        # GUI
        self.OFF_IMAGE = getenv("OFF_IMAGE", OFF_IMAGE)
        self.ON_IMAGE = getenv("ON_IMAGE", ON_IMAGE)
        self.APPLICATION_WIDTH = int(getenv("APPLICATION_WIDTH", 85))
        self.TEXT_SIZE = (int(getenv("TEXT_SIZE_WIDTH", self.APPLICATION_WIDTH * 0.8)), 2)
        self.COMMON_TEXT_AREA_SETTINGS = {
            "bg_color": getenv("COMMON_TEXT_AREA_BG_COLOR", "darkgrey"),
            "text_color":  getenv("COMMON_TEXT_AREA_TEXT_COLOR", "black")
        }

        # Print config
        if self.PRINT_CONFIG is True:
            self.echo_config()

    def echo_config(self):
        for key, value in self.__dict__.items():
            print(f"{key}={value}")


config = ConfigManager()
