import os
import random
import string

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

HONEYFILE_DIR = os.path.join(
    BASE_DIR,
    "demo",
    "vault",
    ".ff_honey"
)

DECOY_NAMES = [
    "passwords.txt",
    "backup_keys.txt",
    "financial_report_2024.docx",
    "credentials.csv",
    "private_notes.txt",
    "company_secrets.pdf",
]

def random_content(size: int = 256) -> str:
    return ''.join(random.choices(string.ascii_letters + string.digits + " \n", k=size))

def generate_honeyfiles():
    os.makedirs(HONEYFILE_DIR, exist_ok=True)

    print("[*] Generating honeyfiles...\n")

    for name in DECOY_NAMES:
        path = os.path.join(HONEYFILE_DIR, name)

        if not os.path.exists(path):
            with open(path, "w", encoding="utf-8") as f:
                f.write(random_content())
            print(f"[+] Honeyfile created: {path}")
        else:
            print(f"[=] Honeyfile exists: {path}")


if __name__ == "__main__":
    generate_honeyfiles()