import json

def filter_vulnerabilities(input_file, service_name, version, cpe_match=None):
    with open(input_file, 'r') as f:
        data = json.load(f)
    
    filtered_vulnerabilities = []
    for item in data.get('vulnerabilities', []):
        cve_item = item.get('cve', {})
        description = cve_item.get("descriptions", [{}])[0].get("value", "").lower()
        configurations = item.get('configurations', {}).get('nodes', [])
        
        match_found = False
        
        if service_name.lower() in description and version.lower() in description:
            match_found = True
        
        if not match_found and cpe_match:
            for config in configurations:
                for match in config.get('cpeMatch', []):
                    if match.get('vulnerable') and cpe_match in match.get('criteria', '').lower():
                        match_found = True
                        break
                if match_found:
                    break
        
        if match_found:
            filtered_vulnerabilities.append(cve_item)
    
    return filtered_vulnerabilities

if __name__ == "__main__":
    filtered_vulns = filter_vulnerabilities("samsung_vulnerabilities.json", "HTTP", "1.1", "cpe:2.3:o:samsung:galaxy_s6")
    for vuln in filtered_vulns:
        print(vuln)
