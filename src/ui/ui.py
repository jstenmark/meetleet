import PySimpleGUI as sg

from src.config_manager import config
from src.ui.constants import OFF_IMAGE

color_settings = (sg.theme_background_color(), sg.theme_background_color())

def create_button(key):
    return sg.Button(
        image_data=OFF_IMAGE,
        border_width=0,
        button_color=sg.theme_background_color(),
        disabled_button_color=sg.theme_background_color(),
        key=f"{key}:button"
    )

def text(text="", btn=None, size=config.TEXT_SIZE):
    return [sg.Text(text, size), btn]

def text_area(text, key, size, bg_color=None, text_color=None):
    return sg.Text(
        text,
        key=key,
        size=size,
        background_color=bg_color if bg_color else "darkgrey",
        text_color=text_color if text_color else "black",
    )


# TRANSCRIPE OUTPUT
def label(text="",key=None):
    return [text_area(text, key=key, size=(int(config.APPLICATION_WIDTH), int(10/5)), **config.COMMON_TEXT_AREA_SETTINGS)]

# GPT RESPONSE TEXTAREAS
def answers(labels, width=config.APPLICATION_WIDTH, height=10, args=config.COMMON_TEXT_AREA_SETTINGS):
    quick_answer = text_area("", key=labels[0], size=(int(width), height))
    full_answer = text_area("", key=labels[1], size=(int(width), int(height*2)))

    return [
        [sg.Text("QUICK")], [quick_answer],
        [sg.Text("FULL!")], [full_answer]
    ]

def create_layout(record_button, analyze_button):
    layout = []
    layout.append(text("[R]ecord", record_button))
    layout.append(text("[A]nalyze", analyze_button))
    layout.append(label("", key="ana_label"))
    layout.extend(answers(["quick_label", "full_label"]))
    layout.append([sg.Button("Exit", key="exit")])
    return layout


