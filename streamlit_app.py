import streamlit as st
import requests
import json

# Securely load the API token from Streamlit Secrets
APPLICATION_TOKEN = st.secrets["APPLICATION_TOKEN"]
BASE_API_URL = "https://api.langflow.astra.datastax.com"
LANGFLOW_ID = "YOUR_LANGFLOW_ID"  # Replace with your Langflow ID
FLOW_ID = "YOUR_FLOW_ID_OR_ENDPOINT_NAME"  # Replace with your Flow ID or Endpoint Name
ENDPOINT = ""  # Optional endpoint name

def run_flow(message: str, tweaks: dict = None):
    """Runs the Langflow flow with the given message and optional tweaks."""
    url = f"{BASE_API_URL}/lf/{LANGFLOW_ID}/api/v1/run/{ENDPOINT or FLOW_ID}"
    headers = {
        "Authorization": f"Bearer {APPLICATION_TOKEN}",
        "Content-Type": "application/json"
    }
    payload = {
        "input_value": message,
        "output_type": "chat",
        "input_type": "chat",
        "tweaks": tweaks or {}
    }
    try:
        response = requests.post(url, headers=headers, json=payload)
        response.raise_for_status()  # Raise an exception for bad status codes
        return response.json()
    except requests.exceptions.RequestException as e:
        st.error(f"Error communicating with the Langflow API: {e}")
        return None

st.title("My Awesome Langflow AI App")

# Sidebar for tweaks
with st.sidebar:
    st.header("AI Behavior Tweaks")
    user_name_tweak = st.text_input("Your Name (for AI context):")
    temperature_tweak = st.slider("Temperature (Creativity):", min_value=0.0, max_value=2.0, value=1.0, step=0.1)

# Main input area
user_message = st.text_area("Enter your message for the AI:", height=150)

if st.button("Send to AI"):
    if user_message:
        st.info("Sending message to the AI...")

        # Prepare tweaks dictionary
        tweaks = {}
        if user_name_tweak:
            tweaks.setdefault("Prompt-RTyGx", {})["user_name"] = user_name_tweak # Replace Prompt-RTyGx if needed
        if temperature_tweak != 1.0:
             tweaks.setdefault("GoogleGenerativeAIModel-p2rNL", {})["temperature"] = temperature_tweak # Replace GoogleGenerativeAIModel-p2rNL if needed

        with st.spinner("Thinking..."):
            response_data = run_flow(user_message, tweaks=tweaks)

        if response_data:
            st.success("AI Response:")
            st.json(response_data) # Display the full JSON response
            # Or, if you know the structure, display specific parts:
            # if response_data and "output" in response_data:
            #     st.write(response_data["output"])
            # elif response_data and "answer" in response_data:
            #     st.write(response_data["answer"])
    else:
        st.warning("Please enter a message.")
