import PySimpleGUI as sg

from assets.constants import OFF_IMAGE
from src import APPLICATION_WIDTH, COMMON_TEXT_AREA_SETTINGS, TEXT_SIZE


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


def create_button(key):
    return sg.Button(
        image_data=OFF_IMAGE,
        border_width=0,
        button_color=(sg.theme_background_color(), sg.theme_background_color()),
        disabled_button_color=(
            sg.theme_background_color(),
            sg.theme_background_color(),
        ),
        key=f"{key}:button"
    )

def create_record_section(record_button):
    return [sg.Text("Start recording: press [r]", size=TEXT_SIZE), record_button]

def create_analysis_section(analyze_button):
    return [sg.Text("Start analysing: press [a]", size=TEXT_SIZE), analyze_button]

def create_label_section():
    return [get_text_area("", "ana_label", size=(APPLICATION_WIDTH, 2), **COMMON_TEXT_AREA_SETTINGS)]

def create_answer_section():
    quick_answer = get_text_area("", "quick_label", size=(APPLICATION_WIDTH, 10), **COMMON_TEXT_AREA_SETTINGS)
    full_answer = get_text_area("", "full_label", size=(APPLICATION_WIDTH, 20), **COMMON_TEXT_AREA_SETTINGS)
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
        [sg.Button("Exit", key="exit")]
    ]

