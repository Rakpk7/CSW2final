import sqlite3
from pathlib import Path

DATA_DIR = Path("data1")
DB_FILE = DATA_DIR / "cw2.db"
USERS_TXT = DATA_DIR / "users.txt"


def create_db():
    conn = sqlite3.connect(DB_FILE)
    conn.execute("""
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT UNIQUE,
            password_hash TEXT,
            role TEXT
        );
    """)
    conn.commit()
    conn.close()


def migrate_users_from_txt():
    """Read users.txt and insert into users table (skip existing)."""
    if not USERS_TXT.exists():
        print("users.txt not found, nothing to migrate.")
        return

    conn = sqlite3.connect(DB_FILE)
    cur = conn.cursor()

    with open(USERS_TXT, "r", encoding="utf-8") as f:
        for line in f:
            line = line.strip()
            if not line:
                continue
            username, pwd_hash, role = line.split(",")
            try:
                cur.execute(
                    "INSERT OR IGNORE INTO users (username, password_hash, role) VALUES (?, ?, ?)",
                    (username, pwd_hash, role)
                )
            except Exception as e:
                print("Error inserting user", username, e)

    conn.commit()
    conn.close()
    print("Migration from users.txt completed.")


if __name__ == "__main__":
    create_db()
    migrate_users_from_txt()
    print("Database initialized and users migrated.")