import streamlit as st
import requests
import json

# Configuration
BASE_API_URL = "https://api.langflow.astra.datastax.com"
LANGFLOW_ID = "50c7cc2c-2232-4c97-b4d1-5b6d38d92ba4"  # Replace with your LangFlow ID
FLOW_ID = "9188fea5-a2be-4301-9f92-f916b23dc9af"  # Replace with your Flow ID
APPLICATION_TOKEN = "AstraCS:asQDxBwpZtXPrurvqluzffPO:da9113aafcfc71137ed7d3dd5d073a081bf21be42c3d7ee49801d760d82508e4"  # Replace with your Application Token

# Function to interact with LangFlow
def run_flow(message, endpoint, tweaks=None):
    api_url = f"{BASE_API_URL}/lf/{LANGFLOW_ID}/api/v1/run/{endpoint}"
    payload = {
        "input_value": message,
        "output_type": "chat",
        "input_type": "chat",
    }
    if tweaks:
        payload["tweaks"] = tweaks

    headers = {
        "Authorization": f"Bearer {APPLICATION_TOKEN}",
        "Content-Type": "application/json",
    }
    response = requests.post(api_url, json=payload, headers=headers)
    return response.json()

# Streamlit UI
st.title("LangFlow API Integration")
user_message = st.text_input("Enter your message:")

if st.button("Submit"):
    if user_message.strip():
        try:
            result = run_flow(
                message=user_message,
                endpoint=FLOW_ID,  # Use flow ID or endpoint name
            )
            st.json(result)
        except Exception as e:
            st.error(f"An error occurred: {e}")
    else:
        st.warning("Please enter a valid message.")

