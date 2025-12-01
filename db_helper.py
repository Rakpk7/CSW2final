import sqlite3
from pathlib import Path
import pandas as pd

DATA_DIR = Path("data1")
DB_FILE = DATA_DIR / "cw2.db"

def connect_db():
    """Create a connection to the SQLite database."""
    return sqlite3.connect(DB_FILE)

# ---------- CYBERSEC INCIDENTS ----------
def create_cyber_table():
    conn = sqlite3.connect(DB_FILE)
    conn.execute("""
        CREATE TABLE IF NOT EXISTS cyber_incidents(
            incident_id INTEGER PRIMARY KEY,
            domain TEXT,
            type TEXT,
            severity TEXT,
            status TEXT,
            reported_at TEXT
        );
    """)
    conn.commit()
    conn.close()

def get_cyber_incidents_df() -> pd.DataFrame:
    conn = sqlite3.connect(DB_FILE)
    df = pd.read_sql_query("SELECT * FROM cyber_incidents", conn)
    conn.close()

    # Normalize only in pandas if column is called "type"
    if "type" in df.columns and "incident_type" not in df.columns:
        df = df.rename(columns={"type": "incident_type"})

    if not df.empty:
        df["reported_at"] = pd.to_datetime(df["reported_at"], errors="coerce")

    return df

def insert_cyber_incident(domain, incident_type, severity, status, reported_at):
    conn = connect_db()
    cur = conn.cursor()
    cur.execute("""
        INSERT INTO cyber_incidents (incident_id, domain, type, severity, status, reported_at)
        VALUES(NULL, ?, ?, ?, ?, ?)
    """, (domain, incident_type, severity, status, reported_at))
    conn.commit()
    conn.close()

# ---------- IT OPERATIONS INCIDENTS ----------
def create_it_table():
    conn = sqlite3.connect(DB_FILE)
    conn.execute("""
        CREATE TABLE IF NOT EXISTS it_incidents(
            incident_id INTEGER PRIMARY KEY,
            service_name TEXT,
            type TEXT,
            severity TEXT,
            status TEXT,
            detected_at TEXT,
            resolved_at TEXT
        );
    """)
    conn.commit()
    conn.close()

def get_it_incidents_df() -> pd.DataFrame:
    conn = sqlite3.connect(DB_FILE)
    df = pd.read_sql_query("SELECT * FROM it_incidents", conn)
    conn.close()

    if "type" in df.columns and "incident_type" not in df.columns:
        df = df.rename(columns={"type": "incident_type"})

    if not df.empty:
        df["detected_at"] = pd.to_datetime(df["detected_at"], errors="coerce")

    return df

def insert_it_incident(service_name, incident_type, severity, status, detected_at, resolved_at=None):
    conn = connect_db()
    cur = conn.cursor()
    cur.execute("""
        INSERT INTO it_incidents (incident_id, service_name, type, severity, status, detected_at, resolved_at)
        VALUES(NULL, ?, ?, ?, ?, ?, ?)
    """, (service_name, incident_type, severity, status, detected_at, resolved_at))
    conn.commit()
    conn.close()

# ---------- USERS TABLE ----------
def create_user_table():
    conn = sqlite3.connect(DB_FILE)
    conn.execute("""
        CREATE TABLE IF NOT EXISTS users(
            id INTEGER PRIMARY KEY,
            username TEXT UNIQUE,
            password_hash TEXT,
            role TEXT
        );
    """)
    conn.commit()
    conn.close()

# Optional migration (from text file) ✅
def migrate_users_from_txt():
    USERS_FILE = DATA_DIR / "users.txt"
    if not USERS_FILE.exists():
        print("users.txt not found, skipping migration.")
        return

    conn = connect_db()
    cur = conn.cursor()

    with open(USERS_FILE, "r", encoding="utf-8") as f:
        for line in f:
            line = line.strip()
            if not line:
                continue
            user, pwd_hash, role = line.split(",")
            cur.execute("INSERT OR IGNORE INTO users VALUES(NULL, ?, ?, ?)", (user, pwd_hash, role))

    conn.commit()
    conn.close()
    print("✅ Users migrated from users.txt")

# ---------- RUN MIGRATIONS ----------
if __name__ == "__main__":
    create_user_table()
    create_cyber_table()
    create_it_table()
    print("✅ All tables created successfully.")