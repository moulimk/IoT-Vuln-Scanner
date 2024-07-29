import sqlite3
import os

DATABASE_PATH = os.path.join(os.path.dirname(__file__), '../data/iot_scanner.db')

def get_db_connection():
    conn = sqlite3.connect(DATABASE_PATH)
    conn.row_factory = sqlite3.Row
    return conn

def initialize_database():
    conn = get_db_connection()
    cursor = conn.cursor()
    
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS devices (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            mac_address TEXT NOT NULL,
            ip_address TEXT NOT NULL,
            manufacturer TEXT,
            device_type TEXT
        )
    ''')
    
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS services (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            device_id INTEGER NOT NULL,
            service_name TEXT,
            service_version TEXT,
            FOREIGN KEY (device_id) REFERENCES devices (id)
        )
    ''')
    
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS vulnerabilities (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            cve_id TEXT,
            description TEXT,
            severity TEXT,
            published_date TEXT,
            last_modified_date TEXT
        )
    ''')
    
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS device_vulnerabilities (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            device_id INTEGER NOT NULL,
            vulnerability_id INTEGER NOT NULL,
            date_detected TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (device_id) REFERENCES devices (id),
            FOREIGN KEY (vulnerability_id) REFERENCES vulnerabilities (id)
        )
    ''')
    
    conn.commit()
    conn.close()

if __name__ == "__main__":
    initialize_database()
