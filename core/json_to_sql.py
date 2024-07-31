import json
import os
from core.database import create_connection, create_tables, insert_device, insert_vulnerability

def load_json(file_path):
    with open(file_path, 'r') as file:
        return json.load(file)

def populate_database_from_json(json_file):
    data = load_json(json_file)
    conn = create_connection('data/devices.db')
    create_tables(conn)
    
    for device_name, vulnerabilities in data.items():
        device_info = device_name.split('_')
        manufacturer = device_info[0]
        device_type = ' '.join(device_info[1:])
        
        # Fetch IP and MAC from the devices table
        cur = conn.cursor()
        cur.execute("SELECT id, ip_address, mac_address FROM devices WHERE device_type = ?", (device_type,))
        device_row = cur.fetchone()
        if device_row:
            device_id, ip_address, mac_address = device_row
            for vulnerability in vulnerabilities:
                insert_vulnerability(conn, vulnerability, device_type)
    
    conn.close()

if __name__ == "__main__":
    json_file_path = 'all_devices_vulnerabilities.json'
    populate_database_from_json(json_file_path)
