import sqlite3

DB_PATH = "backend/database/database.db"

def get_connection():
    return sqlite3.connect(DB_PATH)
