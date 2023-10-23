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
    return sg.Multiline(
        text,
        key=key,
        size=size,
        background_color=bg_color if bg_color else "darkgrey",
        text_color=text_color if text_color else "black",
        disabled=True,  # Make it read-only
        autoscroll=True  # No automatic scrolling
    )

def label(text="", key=None, size=(int(config.APPLICATION_WIDTH), int(10/5))):
    return [text_area(text, key=key, size=size, **config.COMMON_TEXT_AREA_SETTINGS)]

def answers(labels, width=config.APPLICATION_WIDTH, height=10, args=config.COMMON_TEXT_AREA_SETTINGS):
    quick_answer = text_area("", key=labels[0], size=(int(width), height))
    full_answer = text_area("", key=labels[1], size=(int(width), int(height*2)))

    return [
        [sg.Text("QUICK")], [quick_answer],
        [sg.Text("FULL!")], [full_answer]
    ]



