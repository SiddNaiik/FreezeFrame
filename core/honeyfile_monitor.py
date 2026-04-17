import os
import sqlite3
import time
import psutil
from datetime import datetime


from db import DB_NAME, init_db

HONEYFILE_DIR = "./honeyfiles"
SUSPICION_THRESHOLD = 3   # flag alert after this many events

event_counter = {}         # tracks per-process event count

def get_process_accessing_file(file_path: str):
    """
    Tries to find which process has the file open.
    Returns (pid, name) or (None, 'unknown').
    """
    for proc in psutil.process_iter(['pid', 'name', 'open_files']):
        try:
            for f in proc.open_files():
                if file_path in f.path:
                    return proc.pid, proc.name()
        except (psutil.AccessDenied, psutil.NoSuchProcess):
            continue
    return None, "unknown"

def log_event(file_path: str, event_type: str, pid, pname: str, suspicious: int):
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    cursor.execute("""
        INSERT INTO events (file_path, event_type, process_id, process_name, timestamp, suspicious)
        VALUES (?, ?, ?, ?, ?, ?)
    """, (file_path, event_type, pid, pname, datetime.now().isoformat(), suspicious))
    conn.commit()
    conn.close()

def check_suspicion(pid) -> int:
    """Increment counter per process, return 1 if threshold crossed."""
    event_counter[pid] = event_counter.get(pid, 0) + 1
    if event_counter[pid] >= SUSPICION_THRESHOLD:
        return 1
    return 0

def trigger_alert(file_path: str, pid, pname: str, event_type: str):
    print(f"\n🚨 [ALERT] Suspicious activity detected!")
    print(f"   File      : {file_path}")
    print(f"   Event     : {event_type}")
    print(f"   Process   : {pname} (PID: {pid})")
    print(f"   Time      : {datetime.now().isoformat()}")
    print(f"   Action    : Flag process for manual review\n")
    # TODO: plug in Fantoify alert/webhook call here


class HoneyfileHandler(FileSystemEventHandler):

    def on_modified(self, event):
        if not event.is_directory:
            self._handle(event.src_path, "MODIFIED")

    def on_accessed(self, event):
        if not event.is_directory:
            self._handle(event.src_path, "ACCESSED")

    def on_moved(self, event):
        # Rename = strong ransomware indicator
        if not event.is_directory:
            self._handle(event.dest_path, "RENAMED")

    def _handle(self, file_path: str, event_type: str):
        pid, pname = get_process_accessing_file(file_path)
        suspicious = check_suspicion(pid)
        log_event(file_path, event_type, pid, pname, suspicious)

        print(f"[{event_type}] {file_path} | PID: {pid} | Process: {pname} | Suspicious: {bool(suspicious)}")

        if suspicious:
            trigger_alert(file_path, pid, pname, event_type)


def start_monitor():
    init_db()
    observer = Observer()
    handler = HoneyfileHandler()
    observer.schedule(handler, path=HONEYFILE_DIR, recursive=False)
    observer.start()
    print(f"[*] Monitoring honeyfiles in: {HONEYFILE_DIR}")
    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        observer.stop()
    observer.join()

if __name__ == "__main__":
    start_monitor()