import hashlib

class DataAnonymizer:
    @staticmethod
    def anonymize_ip(ip_address):
        hashed_ip = hashlib.sha256(ip_address.encode()).hexdigest()
        return hashed_ip[:8]  # Return a shortened version of the hash

    @staticmethod
    def anonymize_mac(mac_address):
        hashed_mac = hashlib.sha256(mac_address.encode()).hexdigest()
        return hashed_mac[:8]  # Return a shortened version of the hash

# Example usage:
# anonymizer = DataAnonymizer()
# anon_ip = anonymizer.anonymize_ip("192.168.1.1")
# anon_mac = anonymizer.anonymize_mac("00:1A:2B:3C:4D:5E")
# print(f"Anonymized IP: {anon_ip}, Anonymized MAC: {anon_mac}")
