import PySimpleGUI as sg

from src import get_config, logger

config = get_config()
from src.constants import APPLICATION_WIDTH, OFF_IMAGE

TEXT_SIZE = (int(APPLICATION_WIDTH * 0.8), 2)
COMMON_TEXT_AREA_SETTINGS = {"bg_color": "grey", "text_color": "white"}

def get_text_area(text, key, size, bg_color=None, text_color=None):
    bg_color = bg_color if bg_color else sg.theme_background_color()
    text_color = text_color if text_color else "black"
    return sg.Text(
        text,
        key=key,
        size=size,
        background_color=bg_color,
        text_color=text_color,
    )


def create_button():
    return sg.Button(
        image_data=OFF_IMAGE,
        border_width=0,
        button_color=(sg.theme_background_color(), sg.theme_background_color()),
        disabled_button_color=(
            sg.theme_background_color(),
            sg.theme_background_color(),
        ),
    )

def create_record_section(record_button):
    return [sg.Text("Start recording: press [r]", size=TEXT_SIZE), record_button]

def create_analysis_section(analyze_button):
    return [sg.Text("Start analysing: press [a]", size=TEXT_SIZE), analyze_button]

def create_label_section():
    return [get_text_area("", "ana_label", size=(APPLICATION_WIDTH, 2), **COMMON_TEXT_AREA_SETTINGS)]

def create_answer_section():
    quick_answer = get_text_area("", "quick_label", size=(APPLICATION_WIDTH, 5), **COMMON_TEXT_AREA_SETTINGS)
    full_answer = get_text_area("", "full_label", size=(APPLICATION_WIDTH, 12), **COMMON_TEXT_AREA_SETTINGS)
    return [[sg.Text("SHORT ANSWER")], [quick_answer], [sg.Text("LONG ANSWER:")], [full_answer]]

def create_layout(record_button, analyze_button):
    record_section = create_record_section(record_button)
    analysis_section = create_analysis_section(analyze_button)
    label_section = create_label_section()
    answer_section = create_answer_section()
    return [
        record_section,
        analysis_section,
        label_section,
        *answer_section,
        [sg.Button("cancel")]
    ]

