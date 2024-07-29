from scapy.all import ARP, Ether, srp
import pandas as pd
import psutil
import ipaddress
import socket

class ARPScanner:
    def __init__(self):
        self.interface = None
        self.network = None

    def list_interfaces(self):
        return psutil.net_if_addrs().keys()

    def select_interface(self):
        interfaces = self.list_interfaces()
        print("Available interfaces:")
        for i, iface in enumerate(interfaces):
            print(f"{i}. {iface}")
        choice = int(input("Select an interface by number: "))
        self.interface = list(interfaces)[choice]
        print(f"Selected interface: {self.interface}")

        # Determine the network address based on the selected interface
        addrs = psutil.net_if_addrs()[self.interface]
        for addr in addrs:
            if addr.family == socket.AF_INET:
                ip_addr = addr.address
                netmask = addr.netmask
                self.network = ipaddress.IPv4Network(f"{ip_addr}/{netmask}", strict=False)
                print(f"Network address: {self.network}")

    def scan(self):
        if not self.interface:
            raise ValueError("No interface selected.")
        if not self.network:
            raise ValueError("No network address determined.")
        
        print(f"Scanning on interface: {self.interface} in network: {self.network}")

        # Create ARP request packet for the determined network
        arp_request = ARP(pdst=str(self.network))
        broadcast = Ether(dst="ff:ff:ff:ff:ff:ff")
        arp_request_broadcast = broadcast / arp_request

        # Send packet and capture response
        answered_list = srp(arp_request_broadcast, timeout=2, iface=self.interface, verbose=False)[0]

        devices = []
        for sent, received in answered_list:
            devices.append({'ip': received.psrc, 'mac': received.hwsrc})
            print(f"Detected device: IP={received.psrc}, MAC={received.hwsrc}")

        return pd.DataFrame(devices)

# Example usage:
# scanner = ARPScanner()
# scanner.select_interface()
# devices = scanner.scan()
# print(devices)