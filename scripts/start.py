import sys
import os
import json

# Add the project directory to the Python path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from flask import Flask
from core.arp_scanner import ARPScanner
from core.enhanced_device_scanner import EnhancedDeviceScanner
from core.database import create_connection, create_tables, insert_device, insert_vulnerability
from core.data_transfer import transfer_data_to_history, clear_devices_db
from core.json_to_sql import populate_database_from_json
from core.vulnerability_integration import vulnerability_integration

def main():
    # Initialize the database
    transfer_data_to_history()
    clear_devices_db()

    # Prompt user to choose data source
    use_mock = input("Do you want to use mock data? (yes/no): ").strip().lower() == 'yes'
    os.environ['USE_MOCK_ARP_OUTPUT'] = 'True' if use_mock else 'False'
    
    if use_mock:
        from tests.mock_arp_output import mock_arp_output as arp_output
    else:
        print("Initializing ARP Scanner...")
        scanner = ARPScanner()
        print("Selecting interface...")
        scanner.select_interface()
        print("Scanning network...")
        devices = scanner.scan()
        if devices.empty:
            print("No devices found.")
            return
        print(f"Found {len(devices)} devices.")
        enhanced_scanner = EnhancedDeviceScanner()
        detailed_devices = enhanced_scanner.get_device_details(devices)
        arp_output = detailed_devices.to_dict(orient='records')

    # Insert devices into the database
    conn = create_connection('data/devices.db')
    create_tables(conn)
    
    for device in arp_output:
        insert_device(conn, device['ip_address'], device['mac_address'], device['manufacturer'], device['device_type'])
    
    conn.close()
    
    # Run vulnerability integration to create the JSON file
    json_file_path = 'all_devices_vulnerabilities.json'
    if os.path.exists(json_file_path):
        os.remove(json_file_path)
    vulnerability_integration()

    # Populate the database from the JSON file
    populate_database_from_json(json_file_path)

    # Flask app setup
    from ui.device_list import create_device_bp
    print("Setting up Flask app...")
    app = Flask(__name__)
    conn = create_connection('data/devices.db')  # Re-establish connection for Flask app
    app.register_blueprint(create_device_bp(conn))

    # Start Flask server
    print("Starting Flask server...")
    app.run(debug=False)

if __name__ == "__main__":
    main()
