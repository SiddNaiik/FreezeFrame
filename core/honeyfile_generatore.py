import os
import random
import string

HONEYFILE_DIR = "./honeyfiles"

# Decoy names that look attractive to ransomware
DECOY_NAMES = [
    "passwords.txt",
    "backup_keys.txt",
    "financial_report_2024.docx",
    "credentials.csv",
    "private_notes.txt",
    "company_secrets.pdf",
]

def random_content(size: int = 256) -> str:
    """Generate dummy content so file isn't empty."""
    return ''.join(random.choices(string.ascii_letters + string.digits + " \n", k=size))

def generate_honeyfiles():
    os.makedirs(HONEYFILE_DIR, exist_ok=True)
    generated = []

    for name in DECOY_NAMES:
        path = os.path.join(HONEYFILE_DIR, name)
        with open(path, "w", encoding="utf-8") as f:
            f.write(random_content())
        generated.append(path)
        print(f"[+] Honeyfile created: {path}")

    return generated

if __name__ == "__main__":
    generate_honeyfiles()import os
import random
import string

HONEYFILE_DIR = "./honeyfiles"

# Decoy names that look attractive to ransomware
DECOY_NAMES = [
    "passwords.txt",
    "backup_keys.txt",
    "financial_report_2024.docx",
    "credentials.csv",
    "private_notes.txt",
    "company_secrets.pdf",
]

def random_content(size: int = 256) -> str:
    """Generate dummy content so file isn't empty."""
    return ''.join(random.choices(string.ascii_letters + string.digits + " \n", k=size))

def generate_honeyfiles():
    os.makedirs(HONEYFILE_DIR, exist_ok=True)
    generated = []

    for name in DECOY_NAMES:
        path = os.path.join(HONEYFILE_DIR, name)
        with open(path, "w", encoding="utf-8") as f:
            f.write(random_content())
        generated.append(path)
        print(f"[+] Honeyfile created: {path}")

    return generated

if __name__ == "__main__":
    generate_honeyfiles()