from src.config_manager import config
from src.ui.prepare_ui import create_app

if __name__ == "__main__":
    WINDOW = None
    App = create_app(WINDOW)
    config.set_log_output_label(App.WINDOW["-LOG_OUTPUT-"])
    App.run_event_loop()