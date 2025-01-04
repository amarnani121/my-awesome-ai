import requests
import json

BASE_API_URL = "https://api.langflow.astra.datastax.com"
LANGFLOW_ID = "50c7cc2c-2232-4c97-b4d1-5b6d38d92ba4"
FLOW_ID = "9188fea5-a2be-4301-9f92-f916b23dc9af"

def run_flow(message: str, application_token: str, tweaks: dict = None) -> dict:
    api_url = f"{BASE_API_URL}/lf/{LANGFLOW_ID}/api/v1/run/{FLOW_ID}"
    headers = {"Authorization": f"Bearer {application_token}", "Content-Type": "application/json"}
    payload = {
        "input_value": message,
        "output_type": "chat",
        "input_type": "chat",
    }
    if tweaks:
        payload["tweaks"] = tweaks
    response = requests.post(api_url, json=payload, headers=headers)
    return response.json()
