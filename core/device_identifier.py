import pandas as pd

class DeviceIdentifier:
    def __init__(self, oui_file="data/oui.txt"):
        self.oui_data = self.load_oui_data(oui_file)

    def load_oui_data(self, oui_file):
        oui_data = []
        with open(oui_file, 'r') as file:
            lines = file.readlines()
            for i in range(0, len(lines), 4):
                if i + 1 < len(lines):
                    hex_line = lines[i].strip()
                    base16_line = lines[i + 1].strip()
                    if "(hex)" in hex_line:
                        hex_part = hex_line.split()[0].replace('-', ':').lower()
                        organization_name = ' '.join(hex_line.split()[2:])
                        oui_data.append({'assignment': hex_part, 'organization_name': organization_name})
                    elif "(base 16)" in base16_line:
                        base16_part = base16_line.split()[0].lower()
                        organization_name = ' '.join(base16_line.split()[2:])
                        oui_data.append({'assignment': base16_part, 'organization_name': organization_name})
        oui_df = pd.DataFrame(oui_data)
        return oui_df

    def identify(self, mac_address):
        oui_prefix = mac_address.lower()[:8]
        organization = self.oui_data[self.oui_data['assignment'] == oui_prefix]['organization_name']
        if not organization.empty:
            return organization.values[0]
        return "Unknown"

    def map_to_cpe(self, manufacturer, model=None):
        # Simplified mapping logic with realistic CPEs
        cpe_mapping = {
            "Microsoft": "cpe:2.3:o:microsoft:windows_10:1607",
            "Apple": "cpe:2.3:o:apple:ios:14.0",
            # Add more mappings as needed
        }
        return cpe_mapping.get(manufacturer, "Unknown")
