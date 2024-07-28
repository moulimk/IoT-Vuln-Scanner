import requests

class GeminiAPI:
    def __init__(self, api_key):
        self.api_key = api_key
        self.base_url = "https://api.gemini.com"

    def _make_request(self, endpoint, payload):
        url = f"{self.base_url}/{endpoint}"
        headers = {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json"
        }
        response = requests.post(url, json=payload, headers=headers)
        if response.status_code == 200:
            return response.json()
        else:
            response.raise_for_status()

    def get_vulnerability_details(self, vulnerability_id):
        endpoint = "vulnerability/details"
        payload = {"vulnerability_id": vulnerability_id}
        return self._make_request(endpoint, payload)

    def get_security_recommendations(self, vulnerability_details):
        endpoint = "vulnerability/recommendations"
        payload = {"vulnerability_details": vulnerability_details}
        return self._make_request(endpoint, payload)
