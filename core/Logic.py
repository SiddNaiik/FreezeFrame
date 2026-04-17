from honeyfile_detection import process_event
import time
from pprint import pprint
import subprocess

def get_process_name(pid):
    try:
        with open(f"/proc/{pid}/comm", "r") as f:
            return f.read().strip()
    except:
        return f"Unknown ({pid})"

def main():
    # Run the compiled integrate C program
    fanotify = subprocess.Popen(
        ["sudo", "./core/integrate"],
        stdout=subprocess.PIPE,
        text=True,
        bufsize=1
    )

    processes = {}

    print("Monitoring started...\n")

    for i, line in enumerate(fanotify.stdout):
        line = line.strip()
        if not line:
            continue
            
        parts = line.split("|")
        if len(parts) != 3:
            print(f"Skipping malformed line: {line}")
            continue

        pid_str, mask_type, file_path = parts
        
        try:
            pid = int(pid_str)
        except ValueError:
            continue

        process_event(file_path, pid, mask_type)
      
if __name__ == '__main__':
    main()