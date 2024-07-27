import time

class GlobalStats:
    def __init__(self):
        self.total_packets = 0
        self.total_bytes = 0
        self.start_time = time.time()
        self.end_time = self.start_time

    def update_stats(self, packet_length):
        self.total_packets += 1
        self.total_bytes += packet_length
        self.end_time = time.time()

    def get_global_statistics(self):
        total_time = self.end_time - self.start_time
        if total_time == 0:
            return {
                'total_packets': self.total_packets,
                'total_bytes': self.total_bytes,
                'rate_pps': 0,
                'rate_bps': 0
            }
        
        return {
            'total_packets': self.total_packets,
            'total_bytes': self.total_bytes,
            'rate_pps': self.total_packets / total_time,
            'rate_bps': self.total_bytes / total_time
        }
