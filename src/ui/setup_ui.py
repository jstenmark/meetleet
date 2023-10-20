
import PySimpleGUI as sg

from src.ui.simple_ui import ApplicationState, MainApp
from src.ui.ui import create_button, create_layout


def setup_ui(window):
    sg.theme("DarkAmber")
    app_state = ApplicationState(create_button("r"), create_button("a"))
    window = sg.Window(
        "Meetleet ChatGPT",
        create_layout(app_state.rec_state.btn, app_state.ana_state.btn),
        return_keyboard_events=True,
        use_default_focus=False
    )

    return MainApp(app_state, window)
