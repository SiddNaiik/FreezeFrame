import sqlite3
from pathlib import Path

# ✅ Always points to: FreezeFrame/forensics/forensics.db
BASE_DIR = Path(__file__).resolve().parent.parent
DB_PATH = BASE_DIR / "forensics" / "forensics.db"

def get_connection():
    """
    Creates and returns a connection to the SQLite database.
    Ensures the forensics folder exists.
    """
    DB_PATH.parent.mkdir(parents=True, exist_ok=True)
    conn = sqlite3.connect(DB_PATH)
    conn.execute("PRAGMA foreign_keys = ON")
    return conn

def init_db():
    """
    Initializes the database and creates all required tables.
    """
    conn = get_connection()
    cursor = conn.cursor()

    cursor.executescript("""

    CREATE TABLE IF NOT EXISTS frozen_processes (
        id                  INTEGER PRIMARY KEY AUTOINCREMENT,
        timestamp           TEXT NOT NULL,
        pid                 INTEGER NOT NULL,
        process_name        TEXT,
        ppid                INTEGER,
        threat_score        REAL,
        detection_method    TEXT,
        action_taken        TEXT DEFAULT 'SIGSTOP',
        process_state       TEXT,
        notes               TEXT,
        suspicious          INTEGER DEFAULT 0,
        resolved            BOOLEAN DEFAULT 0,
        resolved_action     TEXT,
        resolved_timestamp  TEXT
    );

    CREATE TABLE IF NOT EXISTS threat_events (
        id          INTEGER PRIMARY KEY AUTOINCREMENT,
        timestamp   TEXT NOT NULL,
        pid         INTEGER NOT NULL,
        event_type  TEXT,
        details     TEXT,
        suspicious  INTEGER DEFAULT 0
    );

    CREATE TABLE IF NOT EXISTS files_accessed_before_freeze (
        id                      INTEGER PRIMARY KEY AUTOINCREMENT,
        frozen_process_id       INTEGER NOT NULL,
        file_path               TEXT,
        access_time             TEXT,
        modification_detected   BOOLEAN DEFAULT 0,
        FOREIGN KEY (frozen_process_id) REFERENCES frozen_processes(id)
    );

    CREATE TABLE IF NOT EXISTS process_memory_dumps (
        id                      INTEGER PRIMARY KEY AUTOINCREMENT,
        frozen_process_id       INTEGER NOT NULL,
        dump_path               TEXT,
        dump_timestamp          TEXT,
        file_size_mb            REAL,
        FOREIGN KEY (frozen_process_id) REFERENCES frozen_processes(id)
    );

    CREATE TABLE IF NOT EXISTS admin_actions (
        id              INTEGER PRIMARY KEY AUTOINCREMENT,
        timestamp       TEXT NOT NULL,
        admin_user      TEXT,
        action          TEXT,
        affected_pid    INTEGER,
        reason          TEXT
    );
                         
    CREATE INDEX IF NOT EXISTS idx_pid ON threat_events(pid);
    CREATE INDEX IF NOT EXISTS idx_frozen_pid ON frozen_processes(pid);

    """)

    conn.commit()
    conn.close()

    print(f"✅ Database initialized at: {DB_PATH}")

if __name__ == "__main__":
    init_db()