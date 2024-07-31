import sys
import os
import json

# Add the project directory to the Python path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from core.database import create_connection, create_tables, insert_device, insert_vulnerability

def load_json(file_path):
    with open(file_path, 'r') as file:
        return json.load(file)

def populate_database_from_json(json_file):
    data = load_json(json_file)
    print(f"Loaded JSON data: {data}")
    conn = create_connection('data/devices.db')
    create_tables(conn)
    
    for device_name, vulnerabilities in data.items():
        print(f"Processing device: {device_name}")
        
        # Insert device into the devices table if not already exists
        cur = conn.cursor()
        cur.execute("SELECT id FROM devices WHERE device_type = ?", (device_name,))
        device_row = cur.fetchone()
        
        if not device_row:
            device_id = insert_device(conn, 'unknown', 'unknown', 'unknown', device_name)
        else:
            device_id = device_row[0]
        
        for vulnerability in vulnerabilities:
            print(f"Inserting vulnerability: {vulnerability['id']} for device: {device_name}")
            insert_vulnerability(conn, vulnerability, device_id)
    
    conn.close()
    print("Database population complete.")

if __name__ == "__main__":
    json_file_path = 'all_devices_vulnerabilities.json'
    populate_database_from_json(json_file_path)
