# src/config_manager.py
import json
import os

_instance = None


class Config:
    log_output_label = None

    @classmethod
    def set_log_output_label(cls, label):
        cls.log_output_label = label

    @classmethod
    def log_message(cls, message):
        if cls.log_output_label:
            cls.log_output_label.update(value=message + "\n", append=True)

    def __new__(cls):
        global _instance
        if _instance is None:
            _instance = super(Config, cls).__new__(cls)
        return _instance

    def __init__(self):
        self.CONFIG_FILE = f"{os.getcwd()}/settings.json"
        self.config_data = {}
        self.load_config()
        self.print_config()

    def __getattr__(self, item):
        return self.config_data.get(item, None)

    def set_log_output_label(self, label):
        self.log_output_label = label

    def save_config(self):
        with open(self.CONFIG_FILE, "w") as f:
            json.dump(self.config_data, f, indent=4)

    def load_config(self):
        if os.path.exists(self.CONFIG_FILE):
            with open(self.CONFIG_FILE, "r") as f:
                self.config_data = json.load(f)
        else:
            print(f"{self.CONFIG_FILE} not found. Using default config.")

    def print_config(self):
        if self.config_data.get("PRINT_CONFIG", False):
            output_str = "Configuration:\n"
            for key, value in self.config_data.items():
                output_str += f"{key}={value}\n"
            print(output_str)


config = Config()
