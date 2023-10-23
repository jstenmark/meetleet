import json
import os
from os import getenv
from pathlib import Path

import soundcard as sc
from dotenv import load_dotenv

_instance = None

class Config:
    log_output_label = None

    @classmethod
    def set_log_output_label(cls, label):
        cls.log_output_label = label

    @classmethod
    def log_message(cls, message, log_output_label="-LOG_OUTPUT-"):
        if log_output_label and cls.log_output_label:
            cls.log_output_label.update(value=message+"\n", append=True)



    def __new__(cls):
        global _instance
        if _instance is None:
            _instance = super(Config, cls).__new__(cls)
        return _instance


    def __init__(self):
        self.CONFIG_FILE = "config.json"
        self.load_config()

        FILE_PATH_DOTENV = Path(__file__).resolve().parent / f"../{getenv('FILE_DOTENV', '.env')}"
        load_dotenv(dotenv_path=FILE_PATH_DOTENV)

        # API
        self.OPENAI_API_KEY = getenv("OPENAI_API_KEY")

        # Log Settings
        self.LOG_LEVEL = getenv("LOG_LEVEL", "DEBUG")
        self.PRINT_CONFIG = getenv("PRINT_CONFIG", False)

        # Paths/Files
        self.SRC_PATH = getenv("SRC_PATH")
        self.TMP_DIR = getenv("TMP_DIR")
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
        self.OFF_IMAGE = getenv("OFF_IMAGE","")
        self.ON_IMAGE = getenv("ON_IMAGE", "")
        self.APPLICATION_WIDTH = int(getenv("APPLICATION_WIDTH", 85))
        self.TEXT_SIZE = (int(getenv("TEXT_SIZE_WIDTH", self.APPLICATION_WIDTH * 0.8)), 2)
        self.COMMON_TEXT_AREA_SETTINGS = {
            "bg_color": getenv("COMMON_TEXT_AREA_BG_COLOR", "darkgrey"),
            "text_color":  getenv("COMMON_TEXT_AREA_TEXT_COLOR", "black")
        }

        self.SELECTED_AUDIO_DEVICE = getenv("SELECTED_AUDIO_DEVICE", str(sc.default_speaker().name))
        self.IS_MIC = getenv("IS_MIC", True)


        self.print_config()

    def save_config(self):
        try:
            with open(self.CONFIG_FILE, "w") as f:
                json.dump({"SPEAKER_ID": self.SPEAKER_ID, "SELECTED_AUDIO_DEVICE": self.SELECTED_AUDIO_DEVICE, "IS_MIC": self.IS_MIC}, f)
        except Exception as e:
            print(f"Failed to save config: {e}")

    def load_config(self):
        try:
            if os.path.exists(self.CONFIG_FILE):
                with open(self.CONFIG_FILE, "r") as f:
                    data = json.load(f)
                self.SPEAKER_ID = data.get("SPEAKER_ID", "")
                self.SELECTED_AUDIO_DEVICE = data.get("SELECTED_AUDIO_DEVICE", "")
                self.IS_MIC = data.get("IS_MIC", True)
            else:
                print(f"{self.CONFIG_FILE} not found. Using default config.")
                self.SPEAKER_ID = ""
                self.SELECTED_AUDIO_DEVICE = ""
                self.IS_MIC = True
        except Exception as e:
            print(f"Failed to load config: {e}")


    def print_config(self):
        output_str = "Configuration:\n"
        for key, value in self.__dict__.items():
            output_str += f"{key}={value}\n"

        self.log_message(output_str)


config = Config()
