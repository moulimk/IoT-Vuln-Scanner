import json
import os
import sys
# Add the project directory to sys.path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from core.database import create_connection, create_tables, insert_device, insert_vulnerability

def load_json(file_path):
    with open(file_path, 'r') as file:
        return json.load(file)

def populate_database_from_json(file_path):
    data = load_json(file_path)

    conn = create_connection('data/devices.db')
    create_tables(conn)

    for device_type, vulnerabilities in data.items():
        device_id = insert_device(conn, device_type)
        for vuln in vulnerabilities:
            insert_vulnerability(conn, vuln, device_id)

    conn.close()

if __name__ == "__main__":
    json_file_path = os.path.join(os.path.dirname(__file__), '..', 'all_devices_vulnerabilities.json')
    populate_database_from_json(json_file_path)
