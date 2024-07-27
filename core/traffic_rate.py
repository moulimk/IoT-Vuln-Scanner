import time
import pandas as pd
from scapy.all import sniff

class TrafficRateAnalyzer:
    def __init__(self, interface):
        self.interface = interface
        self.traffic_data = []

    def packet_handler(self, packet):
        if packet.haslayer('IP'):
            src_ip = packet['IP'].src
            self.traffic_data.append({'timestamp': time.time(), 'src_ip': src_ip, 'length': len(packet)})

    def start_analysis(self, duration=60):
        print(f"Starting traffic analysis on {self.interface} for {duration} seconds...")
        sniff(iface=self.interface, prn=self.packet_handler, timeout=duration)
        print("Traffic analysis complete.")

    def get_traffic_statistics(self):
        df = pd.DataFrame(self.traffic_data)
        if df.empty:
            return pd.DataFrame(columns=['src_ip', 'total_packets', 'total_bytes', 'rate_pps', 'rate_bps'])
        
        stats = df.groupby('src_ip').agg(
            total_packets=('length', 'count'),
            total_bytes=('length', 'sum')
        ).reset_index()

        total_time = df['timestamp'].max() - df['timestamp'].min()
        stats['rate_pps'] = stats['total_packets'] / total_time
        stats['rate_bps'] = stats['total_bytes'] / total_time

        return stats

    def get_device_statistics(self, ip_address):
        df = pd.DataFrame(self.traffic_data)
        if df.empty:
            return {'total_packets': 0, 'total_bytes': 0, 'rate_pps': 0, 'rate_bps': 0}
        
        device_df = df[df['src_ip'] == ip_address]
        if device_df.empty:
            return {'total_packets': 0, 'total_bytes': 0, 'rate_pps': 0, 'rate_bps': 0}
        
        total_packets = device_df['length'].count()
        total_bytes = device_df['length'].sum()
        total_time = device_df['timestamp'].max() - device_df['timestamp'].min()
        
        rate_pps = total_packets / total_time if total_time > 0 else 0
        rate_bps = total_bytes / total_time if total_time > 0 else 0
        
        return {
            'total_packets': total_packets,
            'total_bytes': total_bytes,
            'rate_pps': rate_pps,
            'rate_bps': rate_bps
        }
