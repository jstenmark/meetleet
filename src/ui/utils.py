import PySimpleGUI as sg

from src.config_manager import config
from src.ui.constants import OFF_IMAGE

color_settings = (sg.theme_background_color(), sg.theme_background_color())

def create_button(key):
    return sg.Button(
        image_data=OFF_IMAGE,
        border_width=0,
        button_color=(sg.theme_background_color(), sg.theme_background_color()),
        disabled_button_color=(sg.theme_background_color(), sg.theme_background_color()),
        key=f"{key}:button",
        pad=(0,0)
    )

def text(text="", btn=None, size=None):
    size = size if size is not None else (10, 1)  # Default size
    return [sg.Text(text, size), btn]


def text_area(text, key, size=None, bg_color=None, text_color=None, **kwargs):
    size = size if size is not None else (10, 1)  # Default size
    settings = kwargs if kwargs is not None else {}
    return sg.Multiline(
        text,
        key=key,
        size=size,
        background_color=bg_color if bg_color else "darkgrey",
        text_color=text_color if text_color else "black",
        disabled=True,
        autoscroll=True,
        **settings
    )

def label(text="", key=None, size=None):
    size = size if size is not None else (2, 1)  # Default size
    return [text_area(text, key=key, size=size)]

def answers(labels, width=None, height=10):
    width = width if width is not None else 10  # Default width
    quick_answer = text_area("", key=labels[0], size=(int(width), height))
    full_answer = text_area("", key=labels[1], size=(int(width), int(height * 2)))
    return [
        [sg.Text("QUICK")], [quick_answer],
        [sg.Text("FULL!")], [full_answer]
    ]


