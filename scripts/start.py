import sys
import os
import json
from flask import Flask

# Add the project directory to the Python path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from core.arp_scanner import ARPScanner
from core.enhanced_device_scanner import EnhancedDeviceScanner
from core.data_transfer import transfer_data_to_history, clear_devices_db, delete_old_history_data
from core.json_to_sql import populate_database_from_json
from ui.device_list import create_device_bp
from core.vulnerability_integration import vulnerability_integration
from core.database import create_connection, create_tables

def main():
    # Create devices.db with updated schema
    conn = create_connection('data/devices.db')
    create_tables(conn)
    conn.close()

    # Transfer data to history and clear devices.db
    transfer_data_to_history()
    clear_devices_db()

    # Prompt user to choose data source
    use_mock = input("Do you want to use mock data? (yes/no): ").strip().lower() == 'yes'
    
    if not use_mock:
        print("Initializing ARP Scanner...")
        # Initialize ARP Scanner and select interface
        scanner = ARPScanner()
        print("Selecting interface...")
        scanner.select_interface()
        print("Scanning network...")
        devices = scanner.scan()
        
        if devices.empty:
            print("No devices found.")
            return
        
        print(f"Found {len(devices)} devices.")
        
        # Get detailed device information
        print("Gathering detailed device information...")
        enhanced_scanner = EnhancedDeviceScanner()
        detailed_devices = enhanced_scanner.get_device_details(devices)
        
        print(detailed_devices)
        devices_data = detailed_devices.to_dict(orient='records')
    else:
        # Use mock data and run vulnerability integration
        vulnerability_integration()
        json_file_path = 'all_devices_vulnerabilities.json'
        populate_database_from_json(json_file_path)

    # Flask app setup
    print("Setting up Flask app...")
    app = Flask(__name__)
    
    device_bp = create_device_bp(create_connection('data/devices.db'))
    app.register_blueprint(device_bp)
    
    # Start Flask server
    print("Starting Flask server...")
    app.run(debug=False)

if __name__ == "__main__":
    main()
