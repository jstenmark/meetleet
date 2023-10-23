import os
from threading import Event, Lock, Thread

import numpy as np
import PySimpleGUI as sg
from loguru import logger

from src.audio import record_batch
from src.config_manager import config
from src.llm import generate_answer, transcribe_audio
from src.ui.constants import OFF_IMAGE, ON_IMAGE
from src.ui.settings import open_settings_dialog
from src.utils import generate_file_path, save_audio_to_file


class State:
    def __init__(self, btn):
        self.lock, self.btn, self.state = Lock(), btn, False

    def toggle(self):
        with self.lock:
            self.state = not self.state
            self.btn.update(image_data=ON_IMAGE if self.state else OFF_IMAGE)


class AudioState(State):
    def __init__(self):
        super().__init__(None)
        self.filename = None

    def set_filename(self, name):
        with self.lock:
            self.filename = name

    def get_filename(self):
        with self.lock:
            return self.filename


class ApplicationState:
    def __init__(self, rec_btn, ana_btn):
        self.audio_state = AudioState()
        self.rec_state = State(rec_btn)
        self.ana_state = State(ana_btn)
        self.transcript = None


class MainApp:
    def __init__(self, app_state, window):
        self.app_state = app_state
        self.should_run_threads = Event()
        self.should_run_threads.set()
        self.active_threads = []
        self.WINDOW = window


    def handle_toggle_event(self, event, values):
        if not self.should_run_threads.is_set():
            return
        event_name = event.split(":")[0]  # Extract the event name
        state_to_toggle = None
        if event_name == "r":
            state_to_toggle = self.app_state.rec_state
            label = self.WINDOW["-TRANSCRIBE_OUTPUT-"].update
        elif event_name == "a":
            state_to_toggle = self.app_state.ana_state
            label = self.WINDOW["-TRANSCRIBE_OUTPUT-"].update

        if state_to_toggle:
            state_to_toggle.toggle()
            if state_to_toggle.state:
                with state_to_toggle.lock:
                    t = Thread(target=self.background_loop, args=(state_to_toggle, label))
                    self.active_threads.append(t)
                    t.start()

    def background_loop(self, state, update_output_func):
        while self.should_run_threads.is_set() and state.state:

            if state == self.app_state.ana_state:
                res = self.background_analyzing_loop(state,update_output_func)
            elif state == self.app_state.rec_state:
                res = self.background_recording_loop(state, update_output_func)
            if res is False:
                break

    def background_analyzing_loop(self,state,update):
        file_path_audio = self.app_state.audio_state.get_filename()
        try:
            with open(file_path_audio, 'r') as file:  # noqa: F841
                config.log_message("[ANALYZING_LOOP] Starting transcription")
                new_transcript = transcribe_audio(file_path_audio)
                config.log_message(f"[ANALYZING_LOOP] Finished transcription {new_transcript}")
                logger.debug(new_transcript)

            if new_transcript != self.app_state.transcript:
                os.rename(file_path_audio, file_path_audio.replace(config.FILE_NAME_AUDIO, "backup-"+ config.FILE_NAME_AUDIO))
                if new_transcript == "you":
                    state.toggle()
                    config.log_message("[ANALYZING_LOOP] Empty transcript")
                    self.app_state.transcript = None
                    return False
                else:
                    self.app_state.transcript = new_transcript
                    update(self.app_state.transcript)
                    handle_answers(self.app_state.transcript, state, self.WINDOW["-QUICK_OUTPUT-"].update, self.WINDOW["-FULL_OUTPUT-"].update,)

        except (TypeError, FileNotFoundError, Exception):
            state.toggle()
            config.log_message("[ANALYZING_LOOP] Audio file not found")
        return False



    def background_recording_loop(self,state,update):
        update('test window')

        try:
            audio_data_list = []
            while self.should_run_threads.is_set() and state.state:
                audio_sample = record_batch()
                if audio_sample is not None:
                    audio_data_list.append(audio_sample)

            audio_data = np.vstack(audio_data_list)

            if audio_data is None:
                config.log_message("[RECORDING_LOOP] No audio recorded")
                logger.error("[RECORDING_LOOP] No audio data collected")
                return True

            audiopath = generate_file_path(config.FILE_NAME_AUDIO)
            save_audio_to_file(audio_data, audiopath)
            config.log_message(f"[RECORDING_LOOP] Audio saved: {audiopath}")
            logger.debug(f"[RECORDING_LOOP] Audio saved to {audiopath}")
            self.app_state.audio_state.set_filename(audiopath)
        except Exception as e:
            logger.debug(f"[RECORDING_LOOP] background_recording_loop error={e}")
            config.log_message(f"[RECORDING_LOOP] background_recording_loop error={e}")
        return False


    def run_event_loop(self):
        #sg.show_debugger_window()
        while True:
            event, values = self.WINDOW.read(timeout=10)
            if event in [sg.WIN_CLOSED, "exit"]:
                break

            if event == 'General':
                #config.log_message(f"Event: {event}, Values: {values}\n", "-LOG_OUTPUT-")
                open_settings_dialog()

            #if event ==
            else:
                self.handle_toggle_event(event,values)

        # exit the app
        self.should_run_threads.clear()
        for t in self.active_threads:
            t.join()
        self.active_threads.clear()
        self.WINDOW.close()
        exit(0)



def handle_answers(transcript, state, quick_update, full_update):
    if transcript is None:
        return
    lock = Lock()
    finished_threads = 0

    def response(target, short, temp):
        nonlocal finished_threads
        text = "Chatgpt is working..."
        target.update(text)

        ans = generate_answer(transcript, short, temp)
        target.update(ans)

        with lock:
            finished_threads += 1
            if finished_threads == 2:  # Check if all threads are done
                state.toggle()

    Thread(target=response, args=(quick_update, True, 0)).start()
    Thread(target=response, args=(full_update, False, 0.7)).start()
