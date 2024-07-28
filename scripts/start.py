# scripts/start.py

import sys
import os
from flask import Flask

# Add the project directory to sys.path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from core.arp_scanner import ARPScanner
from core.device_identifier import DeviceIdentifier
from core.traffic_rate import TrafficRateAnalyzer
from core.anonymization import DataAnonymizer
from core.global_stats import GlobalStats
import ui.device_list as device_list_ui
from ui.device_list import device_bp, set_devices, set_traffic_analyzer, set_global_stats, set_ip_map
from ui.consent import consent_bp
from ui.sidebar import sidebar_bp
import pandas as pd

def main():
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
    
    # Initialize Device Identifier
    print("Initializing Device Identifier...")
    identifier = DeviceIdentifier(oui_file="data/oui.txt")

    # Identify devices and anonymize data
    anonymizer = DataAnonymizer()
    device_data = []
    original_ip_map = {}
    for index, device in devices.iterrows():
        manufacturer = identifier.identify(device['mac'])
        anon_ip = anonymizer.anonymize_ip(device['ip'])
        anon_mac = anonymizer.anonymize_mac(device['mac'])
        device_data.append({'ip': anon_ip, 'mac': anon_mac, 'manufacturer': manufacturer})
        original_ip_map[anon_ip] = device['ip']  # Map anonymized IP to original IP
        print(f"IP: {anon_ip}, MAC: {anon_mac}, Manufacturer: {manufacturer}")
    
    device_df = pd.DataFrame(device_data)
    set_devices(device_df)

    # Start Traffic Analysis
    print("Starting traffic analysis...")
    analyzer = TrafficRateAnalyzer(interface=scanner.interface)
    global_stats = GlobalStats()
    analyzer.start_analysis(duration=60)
    for packet in analyzer.traffic_data:
        global_stats.update_stats(packet['length'])
    
    stats = analyzer.get_traffic_statistics()
    print("Traffic Statistics:")
    print(stats)

    global_stats_data = global_stats.get_global_statistics()
    print("Global Traffic Statistics:")
    print(global_stats_data)

    # Pass Traffic Analyzer and IP Map to UI
    set_traffic_analyzer(analyzer)
    set_global_stats(global_stats)
    set_ip_map(original_ip_map)

    # Create Flask app and register blueprints
    app = Flask(__name__, template_folder='../ui/templates')
    app.register_blueprint(device_bp)
    app.register_blueprint(consent_bp)
    app.register_blueprint(sidebar_bp)

    # Start Flask server
    print("Starting Flask server...")
    app.run(debug=False)

if __name__ == "__main__":
    main()
