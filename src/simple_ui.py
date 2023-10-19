import os
from threading import Event, Lock, Thread

import numpy as np
import PySimpleGUI as sg

from src import config, logger
from src.audio import record_batch, save_audio_file
from src.constants import OFF_IMAGE, ON_IMAGE
from src.llm import generate_answer, transcribe_audio
from src.ui import create_button, create_layout
from src.utils import generate_audio_path


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
    def __init__(self, app_state):
        self.app_state = app_state
        self.should_run_threads = Event()
        self.should_run_threads.set()
        self.event_handlers = {
            "cancel": self.handle_cancel_event,
            "r": self.handle_recording_event,
            "a": self.handle_analysis_event,
        }

    def handle_recording_event(self, event, values):
        self.app_state.rec_state.toggle()
        if self.app_state.rec_state.state:
            with self.app_state.rec_state.lock:
                Thread(target=self.background_recording_loop).start()

    def handle_analysis_event(self, event, values):
        self.app_state.ana_state.toggle()
        if self.app_state.ana_state.state:
            with self.app_state.ana_state.lock:
                Thread(target=self.background_analyzing_loop).start()

    def background_analyzing_loop(self):
        label = WINDOW["ana_label"]
        while self.should_run_threads.is_set() and self.app_state.ana_state.state:
            file_path_audio = self.app_state.audio_state.get_filename()

            try:
                with open(file_path_audio, 'r') as file:
                    pass
            except TypeError:
                self.app_state.ana_state.toggle()
                label.update("No audio file to analyze")
                break
            except FileNotFoundError:
                self.app_state.ana_state.toggle()
                label.update("No audio file to analyze")
                break

            label.update("Start analyzing...")
            new_transcript = transcribe_audio(file_path_audio)
            if new_transcript != self.app_state.transcript:
                logger.debug(new_transcript)
                os.remove(file_path_audio)
                if new_transcript == "you":
                    self.app_state.ana_state.toggle()
                    label.update("ERROR: empty transcript")
                    break
                label.update(new_transcript)
                self.app_state.transcript = new_transcript
                handle_answers(new_transcript, self.app_state.ana_state)
                break

    def background_recording_loop(self):
        try:
            audio_data_list = []
            while self.should_run_threads.is_set() and self.app_state.rec_state.state:
                audio_sample = record_batch()
                if audio_sample is not None:
                    audio_data_list.append(audio_sample)

            audio_data = np.vstack(audio_data_list)

            if audio_data is None:
                logger.error("[AUDIO] No audio data collected")
                return

            audiopath = generate_audio_path()
            save_audio_file(audio_data, audiopath)
            logger.debug(f"[AUDIO] Audio saved to {audiopath}")
            self.app_state.audio_state.set_filename(audiopath)
        except Exception as e:
            pass

    def handle_cancel_event(self, event, values):
        self.should_run_threads = False
        WINDOW.close()
        exit(0)

    def run_event_loop(self, window):
        while True:
            event, values = window.read()
            if event == sg.WIN_CLOSED:
                break
            event_name = event.split(":")[0] if ":" in event else event
            handler = self.event_handlers.get(event_name.lower())
            if handler:
                handler(event, values)
        window.close()


def handle_answers(transcript, state):
    if transcript is None:
        return

    lock = Lock()
    finished_threads = 0

    def response(target, short, temp):
        nonlocal finished_threads
        target.update("Chatgpt is working...")
        ans = generate_answer(transcript, short, temp)
        target.update(ans)

        with lock:
            finished_threads += 1
            if finished_threads == 2:  # Check if all threads are done
                state.toggle()

    Thread(target=response, args=(WINDOW["quick_label"], True, 0)).start()
    Thread(target=response, args=(WINDOW["full_label"], False, 0.7)).start()


if __name__ == "__main__":
    sg.theme("DarkAmber")
    app_state = ApplicationState(create_button("r"), create_button("a"))

    layout = create_layout(app_state.rec_state.btn, app_state.ana_state.btn)

    WINDOW = sg.Window(
        "Meetleet ChatGPT", layout, return_keyboard_events=True, use_default_focus=False
    )

    app = MainApp(app_state)
    app.run_event_loop(WINDOW)

