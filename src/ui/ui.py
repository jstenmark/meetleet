import PySimpleGUI as sg

from src.config_manager import config


def text_area(text, key, size, bg_color=None, text_color=None):
    bg_color = bg_color if bg_color else "darkgrey"
    text_color = text_color if text_color else "black"

    return sg.Text(
        text,
        key=key,
        size=size,
        background_color=bg_color,
        text_color=text_color,
    )


def create_button(key):
    color_settings = (sg.theme_background_color(), sg.theme_background_color())
    return sg.Button(
        image_data=config.OFF_IMAGE,
        border_width=0,
        button_color=color_settings,
        disabled_button_color=color_settings,
        key=f"{key}:button"
    )

def text(text="MISSING_TEXT_FOR_FIELD", label="", size=config.TEXT_SIZE, btn=None, **kwargs):
    frame_layout = [
        [sg.Text(text, size)]
    ]
    bg_color = kwargs.get('bg_color', sg.theme_background_color())
    frame = [sg.Frame("", frame_layout, background_color=bg_color, border_width=0)]
    if btn:
        frame.append(btn)
    return frame



# TRANSCRIPE OUTPUT
def label(text="",key=None, width=config.APPLICATION_WIDTH, height=10, args=config.COMMON_TEXT_AREA_SETTINGS):
    return [text_area(text, key=key, size=(int(width), int(height/5)), **args)]

# GPT RESPONSE TEXTAREAS
def answers(labels, width=config.APPLICATION_WIDTH, height=10, args=config.COMMON_TEXT_AREA_SETTINGS):
    quick_answer = text("", label=labels[0], size=(int(width), height), **args)
    full_answer = text("", label=labels[1], size=(int(width), int(height*2)), **args)
    return [
        [sg.Text(labels[0].split("_")[0]), *quick_answer],
        [sg.Text(labels[1].split("_")[0]), *full_answer]
    ]

def create_layout(record_button, analyze_button):
    layout = []
    layout.append(text(text="[R]ecord", btn=record_button))
    layout.append(text(text="[A]nalyze", btn=analyze_button))
    layout.append(label(text="", key="ana_label"))
    layout.extend(answers(["quick_label", "full_label"]))
    layout.append([sg.Button("Exit", key="exit")])
    return layout


