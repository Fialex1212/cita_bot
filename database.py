import sqlite3
import os


def create_table():
    db_path = "/app/database.db"
    if not os.path.exists(db_path):
        print(f"Database file {db_path} does not exist. Creating a new one.")
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    cursor.execute(
        """
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            telegram_id INTEGER NOT NULL,
            username TEXT NOT NULL
        )
    """
    )
    conn.commit()
    conn.close()


def add_user(telegram_id, username):
    create_table()
    db_path = "/app/database.db"
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    cursor.execute(
        "INSERT OR IGNORE INTO users (telegram_id, username) VALUES (?, ?)",
        (telegram_id, username),
    )
    conn.commit()
    conn.close()
