import os

BASE_DIR = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

HONEY_DIR = os.path.join(BASE_DIR, "demo", "vault", ".ff_honey")

HONEY_PATHS = [
    os.path.join(HONEY_DIR, "passwords.txt"),
    os.path.join(HONEY_DIR, "backup_keys.txt"),
    os.path.join(HONEY_DIR, "financial_report_2024.docx"),
    os.path.join(HONEY_DIR, "credentials.csv"),
    os.path.join(HONEY_DIR, "private_notes.txt"),
    os.path.join(HONEY_DIR, "company_secrets.pdf"),
]

def normalize_path(p: str) -> str:
    return os.path.normcase(os.path.realpath(os.path.normpath(p)))

HONEY_REALPATHS = {normalize_path(p) for p in HONEY_PATHS}


def process_event(event_path, pid, mask_type):
    event_real = normalize_path(event_path)
    is_honey = event_real in HONEY_REALPATHS

    if is_honey:
        print("🚨 HONEYFILE ACCESSED!")
        print("PID:", pid)
        print("EVENT:", mask_type)
        print("FILE:", event_path)
        return True
    else:
        pass
    return False


def get_process_name(pid):
    try:
        with open(f"/proc/{pid}/comm", "r", encoding="utf-8", errors="ignore") as f:
            return f.read().strip()
    except Exception:
        return f"Unknown ({pid})"
