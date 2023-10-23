
import PySimpleGUI as sg

from src.config_manager import config
from src.ui.simple_ui import ApplicationState, MainApp
from src.ui.utils import answers, create_button, label, text


def create_layout(record_button, analyze_button):
    menu_row = [sg.Menu([
        ['File', ['Exit']],
        ['Settings', ['General']],
        ['Debug', ['Debug']]
    ])]

    column1 = [
        text("[R]ecord", record_button),
        text("[A]nalyze", analyze_button),
        label("\n", key="-TRANSCRIBE_OUTPUT-", size=(int(config.APPLICATION_WIDTH), 20)),
        label("\n", key="-LOG_OUTPUT-", size=(int(config.APPLICATION_WIDTH), 20))
    ]

    column2 = answers(["-QUICK_OUTPUT-", "-FULL_OUTPUT-"])

    prompt_row = [
        sg.Button("Load chat session", key="-LoadSession-"),
        sg.Button("Save chat session", key="-SaveSession-"),
    ],

    button_row = [sg.Button("Exit", key="exit")]
    layout = [
        [menu_row],
        [sg.Column(column1, vertical_alignment='top'), sg.VerticalSeparator(), sg.Column(column2, vertical_alignment='top')],
        [prompt_row],
        [button_row],
    ]

    return layout


def create_app(title="MeetLeet", WINDOW=None):
    sg.theme("DarkAmber")

    record_button = create_button("r")
    analyze_button = create_button("a")

    state = ApplicationState(record_button,analyze_button)
    layout = create_layout(state.rec_state.btn, state.ana_state.btn)


    WINDOW = sg.Window(title,layout,return_keyboard_events=True, use_default_focus=False, resizable=True) # transparent_color = None ??

    return MainApp(state, WINDOW)

