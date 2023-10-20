


from src.ui.setup_ui import setup_ui

if __name__ == "__main__":
    WINDOW = None
    main = setup_ui(WINDOW)
    main.run_event_loop()