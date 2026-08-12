"""Safety-net cleanup for the temp folder.

The tools process images in memory and never write to disk, so this folder
should stay empty in normal use. But if you extend the app to save files,
this background thread sweeps out anything older than TEMP_FILE_MAX_AGE_MIN
so nothing accumulates.
"""
import os
import time
import threading

from config import UPLOAD_FOLDER, TEMP_FILE_MAX_AGE_MIN


def _sweep_once():
    if not os.path.isdir(UPLOAD_FOLDER):
        return
    cutoff = time.time() - TEMP_FILE_MAX_AGE_MIN * 60
    for name in os.listdir(UPLOAD_FOLDER):
        if name == ".gitkeep":
            continue
        path = os.path.join(UPLOAD_FOLDER, name)
        try:
            if os.path.isfile(path) and os.path.getmtime(path) < cutoff:
                os.remove(path)
        except OSError:
            pass  # file vanished or is locked — ignore and move on


def start_cleanup_thread(interval_seconds: int = 300):
    """Start a daemon thread that sweeps the temp folder periodically."""
    def loop():
        while True:
            _sweep_once()
            time.sleep(interval_seconds)

    thread = threading.Thread(target=loop, daemon=True)
    thread.start()
    return thread
