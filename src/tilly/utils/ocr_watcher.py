import time
import os
from ocr import batch_process_folder, logging

WATCH_FOLDER = "data/screenshots"
PROCESSED_FOLDER = "data/screenshots/processed"

os.makedirs(PROCESSED_FOLDER, exist_ok=True)

def move_processed(file_path: str):
    base = os.path.basename(file_path)
    os.rename(file_path, os.path.join(PROCESSED_FOLDER, base))

def watch_folder():
    logging.info(f"Watching folder: {WATCH_FOLDER}")
    processed = set()
    while True:
        files = [f for f in os.listdir(WATCH_FOLDER) if f.lower().endswith((".png", ".jpg", ".jpeg", ".bmp"))]
        new_files = set(files) - processed
        if new_files:
            for f in new_files:
                full_path = os.path.join(WATCH_FOLDER, f)
                batch_process_folder(WATCH_FOLDER)
                move_processed(full_path)
                processed.add(f)
        time.sleep(5)  # check every 5 seconds

if __name__ == "__main__":
    watch_folder()
