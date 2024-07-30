import sqlite3
from datetime import datetime, timedelta

def create_connection(db_file):
    conn = sqlite3.connect(db_file)
    return conn

def create_history_tables(conn):
    with conn:
        conn.execute('''
            CREATE TABLE IF NOT EXISTS devices (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                ip_address TEXT,
                mac_address TEXT,
                manufacturer TEXT,
                device_type TEXT,
                transfer_date TEXT
            )
        ''')
        conn.execute('''
            CREATE TABLE IF NOT EXISTS vulnerabilities (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                device_id INTEGER,
                ip_address TEXT,
                mac_address TEXT,
                cve_id TEXT,
                description TEXT,
                severity TEXT,
                published_date TEXT,
                last_modified_date TEXT,
                transfer_date TEXT,
                FOREIGN KEY (device_id) REFERENCES devices(id)
            )
        ''')

def transfer_data_to_history():
    devices_conn = create_connection('data/devices.db')
    history_conn = create_connection('data/history.db')

    create_history_tables(history_conn)

    devices = devices_conn.execute('SELECT * FROM devices').fetchall()
    vulnerabilities = devices_conn.execute('SELECT * FROM vulnerabilities').fetchall()

    print("Devices fetched from devices.db:", devices)  # Debug print statement

    for device in devices:
        if len(device) < 5:
            print("Device tuple has fewer elements than expected:", device)
            continue
        history_conn.execute('''
            INSERT INTO devices (ip_address, mac_address, manufacturer, device_type, transfer_date)
            VALUES (?, ?, ?, ?, ?)
        ''', (device[1], device[2], device[3], device[4], datetime.now()))

    for vuln in vulnerabilities:
        history_conn.execute('''
            INSERT INTO vulnerabilities (device_id, ip_address, mac_address, cve_id, description, severity, published_date, last_modified_date, transfer_date)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
        ''', (vuln[1], vuln[2], vuln[3], vuln[4], vuln[5], vuln[6], vuln[7], vuln[8], datetime.now()))

    devices_conn.commit()
    history_conn.commit()

    devices_conn.close()
    history_conn.close()

def clear_devices_db():
    conn = create_connection('data/devices.db')
    with conn:
        conn.execute('DELETE FROM devices')
        conn.execute('DELETE FROM vulnerabilities')
    conn.commit()
    conn.close()

def delete_old_history_data():
    conn = create_connection('data/history.db')
    one_week_ago = (datetime.now() - timedelta(weeks=1)).isoformat()
    with conn:
        conn.execute('DELETE FROM devices WHERE transfer_date < ?', (one_week_ago,))
        conn.execute('DELETE FROM vulnerabilities WHERE transfer_date < ?', (one_week_ago,))
    conn.commit()
    conn.close()

if __name__ == "__main__":
    delete_old_history_data()
