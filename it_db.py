import sqlite3
from pathlib import Path
import pandas as pd

DATA_DIR = Path("data1")
DATA_DIR.mkdir(exist_ok=True)

DB_FILE = DATA_DIR / "cw2.db"
IT_CSV_FILE = DATA_DIR / "it_incidents.csv"


def create_it_incidents_table():
    """Create IT incidents table if it does not exist."""
    conn = sqlite3.connect(DB_FILE)
    conn.execute(
        """
        CREATE TABLE IF NOT EXISTS it_incidents (
            incident_id INTEGER PRIMARY KEY,
            service_name TEXT,
            incident_type TEXT,
            severity TEXT,
            status TEXT,
            detected_at TEXT,
            resolved_at TEXT
        );
        """
    )
    conn.commit()
    conn.close()


def load_it_incidents_csv():
    """Load data from it_incidents.csv into it_incidents table."""
    if not IT_CSV_FILE.exists():
        print("it_incidents.csv not found – skipping load.")
        return

    df = pd.read_csv(IT_CSV_FILE)

    conn = sqlite3.connect(DB_FILE)
    # write DataFrame to SQLite (replace old content)
    df.to_sql("it_incidents", conn, if_exists="replace", index=False)
    conn.close()
    print("IT incidents CSV loaded into it_incidents table.")


if __name__ == "__main__":
    create_it_incidents_table()
    load_it_incidents_csv()
    print("IT incidents table ready.")