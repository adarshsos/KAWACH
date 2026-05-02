import sqlite3
import os

DB_PATH = os.path.join(os.path.dirname(__file__), 'kawach.db')

def init_db():
    """
    Initializes the SQLite Database schema for KAWACH.
    This hybrid database structure uses local SQLite for encrypted vault storage,
    ensuring maximum user privacy as requested in the system architecture.
    """
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    
    # User accounts schema
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT UNIQUE NOT NULL,
            password_hash TEXT NOT NULL, -- bcrypt hashed
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    ''')
    
    # Encrypted vault schema
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS vault (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER NOT NULL,
            website TEXT NOT NULL,
            username TEXT NOT NULL,
            encrypted_password TEXT NOT NULL, -- AES-256 encrypted
            iv TEXT NOT NULL, -- Initialization Vector for AES
            FOREIGN KEY (user_id) REFERENCES users (id)
        )
    ''')
    
    # Scan history schema
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS scan_history (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER NOT NULL,
            cyber_health_score INTEGER NOT NULL,
            device_risks_found INTEGER NOT NULL,
            network_risks_found INTEGER NOT NULL,
            scan_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (user_id) REFERENCES users (id)
        )
    ''')
    
    conn.commit()
    conn.close()

def get_db_connection():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn
