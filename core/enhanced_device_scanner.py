import nmap
import pandas as pd
import os
import json
import sys
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from core.device_identifier import DeviceIdentifier
from core.database import create_connection

class EnhancedDeviceScanner:
    def __init__(self, oui_file="data/oui.txt"):
        self.identifier = DeviceIdentifier(oui_file=oui_file)
        self.nm = nmap.PortScanner()

    def get_device_details(self, devices):
        detailed_devices = []

        for index, device in devices.iterrows():
            ip = device['ip']
            mac = device['mac']
            manufacturer = self.identifier.identify(mac)

            # Nmap service scan
            self.nm.scan(ip, arguments='-sV')
            services = []
            for proto in self.nm[ip].all_protocols():
                lport = self.nm[ip][proto].keys()
                for port in lport:
                    service = self.nm[ip][proto][port]['name']
                    version = self.nm[ip][proto][port]['version']
                    services.append({"service": service, "version": version})

            detailed_device = {
                "mac_address": mac,
                "ip_address": ip,
                "manufacturer": manufacturer,
                "services": services
            }
            detailed_devices.append(detailed_device)

        self.save_devices(detailed_devices)
        return pd.DataFrame(detailed_devices)

    def save_devices(self, devices):
        output_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', 'tests', 'arp_output.py')
        with open(output_path, 'w') as file:
            file.write('arp_output = ' + json.dumps(devices, indent=4))

# Usage example
if __name__ == "__main__":
    from core.arp_scanner import ARPScanner

    arp_scanner = ARPScanner()
    devices = arp_scanner.scan()

    if not devices.empty:
        enhanced_scanner = EnhancedDeviceScanner()
        detailed_devices = enhanced_scanner.get_device_details(devices)
        print(detailed_devices)
    else:
        print("No devices found.")
