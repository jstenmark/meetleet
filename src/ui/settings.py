
import PySimpleGUI as sg
import soundcard as sc

from src.config_manager import config


def open_settings_dialog():
    audio_device_list = [(True, mic.name) for mic in sc.all_microphones()] + [(False, sp.name) for sp in sc.all_speakers()]
    device_names = [name for is_mic, name in audio_device_list]

    layout = [
        [sg.Text('Settings')],
        [sg.Text('Audio Device'), sg.Combo(device_names, default_value=config.SELECTED_AUDIO_DEVICE, key='audio_device')],
        [sg.Text('Example Setting 1'), sg.Input(key='setting1')],
        [sg.Button('Save'), sg.Button('Cancel')]
    ]

    window = sg.Window('Settings', layout)

    while True:
        event, values = window.read()
        if event in (sg.WIN_CLOSED, 'Cancel'):
            break
        if event == 'Debug':
            sg.show_debugger_popout_window()
        if event == 'Save':
            selected_device = values['audio_device']
            config.SELECTED_AUDIO_DEVICE = selected_device
            config.IS_MIC = any(is_mic and name == selected_device for is_mic, name in audio_device_list)
            config.example_setting_1 = values['setting1']
            break

    window.close()