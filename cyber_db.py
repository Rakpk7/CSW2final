import sqlite3
from pathlib import Path
import pandas as pd

DATA_DIR = Path("data1")
DB_FILE = DATA_DIR / "cw2.db"

def connect_db():
    return sqlite3.connect(DB_FILE)

def get_it_incidents_df() -> pd.DataFrame:
    """Fetch all IT incidents from the database"""
    conn = connect_db()
    try:
        df = pd.read_sql_query("SELECT * FROM it_incidents", conn)
    except Exception:
        df = pd.DataFrame()  # return empty instead of crashing
    conn.close()
    return df