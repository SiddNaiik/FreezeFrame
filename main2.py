import subprocess
import time

gen = subprocess.Popen(["python3", "./core/honeyfile_generator.py"])

gen.wait()

print("\n[*] Starting fanotify engine...")
logic = subprocess.Popen(["python3", "./core/Logic.py"])

print("\n[*] Freezeframe running...\n")
print("[*] Press Ctrl+C to stop\n")

try:
    while True:
        time.sleep(5)
except KeyboardInterrupt:
    print("\nStopping Freezeframe...")
    logic.kill()