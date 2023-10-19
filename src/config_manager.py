import os
from pathlib import Path

from dotenv import load_dotenv


class ConfigManager:
    def __init__(self):

        env_path = os.path.join(os.path.dirname(__file__), '../.env')
        load_dotenv(dotenv_path=env_path)

        self.OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
        self.LOG_LEVEL = os.getenv("LOG_LEVEL", "DEBUG")


config = ConfigManager()
