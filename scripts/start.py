import sys
import os
from flask import Flask

# Add the project directory to sys.path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from core.arp_scanner import ARPScanner
from core.enhanced_device_scanner import EnhancedDeviceScanner
from core.database import initialize_database
from ui.device_list import create_device_bp

devices_data = None  # Global variable to store devices data

def main():
    global devices_data

    # Initialize the database
    initialize_database()

    # Prompt user to choose data source
    use_mock = input("Do you want to use mock data? (yes/no): ").strip().lower() == 'yes'
    os.environ['USE_MOCK_ARP_OUTPUT'] = 'True' if use_mock else 'False'
    
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
        # Use mock data
        from tests.mock_arp_output import mock_arp_output
        devices_data = mock_arp_output

    # Flask app setup
    print("Setting up Flask app...")
    app = Flask(__name__)
    app.config['devices'] = devices_data
    
    device_bp = create_device_bp()
    app.register_blueprint(device_bp)
    
    # Start Flask server
    print("Starting Flask server...")
    app.run(debug=False)

if __name__ == "__main__":
    main()
