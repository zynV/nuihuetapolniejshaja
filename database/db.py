import sqlite3
import os

os.makedirs("database", exist_ok=True)

def init_db():
    conn = sqlite3.connect("database/auth.db")
    cursor = conn.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS users (
            patreon_id TEXT PRIMARY KEY,
            telegram_id TEXT,
            email TEXT,
            access_token TEXT,
            tier TEXT,
            joined_channel INTEGER DEFAULT 0,
            expires_at TEXT
        )
    """)
    conn.commit()
    conn.close()
