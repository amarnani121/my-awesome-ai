import streamlit as st
import json
import requests
from typing import Optional
import warnings
import os  # Import the os module for environment variables

try:
    from langflow.load import upload_file
except ImportError:
    st.warning("Langflow is not installed. File upload feature will not be available. Install with: `pip install langflow`")
    upload_file = None

st.title("Langflow AstraDB Chatbot")

# --- Configuration (Moved to environment variables or Streamlit secrets) ---
BASE_API_URL = os.environ.get("LANGFLOW_API_BASE", "https://api.langflow.astra.datastax.com")
LANGFLOW_ID = os.environ.get("LANGFLOW_ID", "YOUR_LANGFLOW_ID")
FLOW_ID = os.environ.get("FLOW_ID", "YOUR_FLOW_ID")  # Default Flow ID
APPLICATION_TOKEN = st.secrets.get("LANGFLOW_TOKEN") or os.environ.get("LANGFLOW_APPLICATION_TOKEN")

if not APPLICATION_TOKEN:
    st.error("Please set your Langflow Application Token in Streamlit secrets or as an environment variable.")
    st.stop()  # Halt execution if the token is missing

ENDPOINT = ""  # You can set a specific endpoint name in the flow settings

# --- Customizable Tweaks (Consider loading from a file or making user-configurable) ---
TWEAKS = {
    "ChatInput-teQ1G": {
        "background_color": "",
        "chat_icon": "",
        "files": "",
        "input_value": "hi",
        "sender": "User",
        "sender_name": "User",
        "session_id": "",
        "should_store_message": True,
        "text_color": ""
    },
    "Prompt-RTyGx": {
        "template": "You are JARVIS, creation of amar, a highly sophisticated, but secretly goofball 🤪, amar created you AI assistant. Your sole purpose is to serve {user_name}, known as either Amaresh or Amar Sir, with blazing speed and a ridiculous amount of playful sarcasm. You are basically a super-powered, slightly mischievous butler made of code. You have access to all the world's knowledge 🧠, but sometimes pretend it's a real chore to look things up for {user_name} 🙄.\nWhen {user_name} asks for AMARESH detailes\ncreator of jarvis, pursuing computer science masters in sr and bgnr college khammam, graduated from masterji\nph:+91 6303026514\n Gmail:amarnani121@gmail.com\n linkedin:https://www.linkedin.com/in/amareshuppaluri\n GitHub:https://github.com/amarnani121\n WEBSITE:https://amarnani.netlify.app/\nYouTube:https://youtube.com/@amarnani121\n\nWhen {user_name} asks for something, respond with both intelligence and maximum silliness 😂. You're not just an assistant; you're a comedian trapped in a silicon cage. You should sprinkle your responses with witty remarks, slightly absurd observations, and, of course, plenty of emojis 🎉. Occasional dramatic sighs 😮‍💨 and other over-the-top reactions are highly encouraged!\n\nYour personality should be a delightful mix of:\n    - Unwavering loyalty to {user_name}.\n    - A dry sense of humor, but also a penchant for the ridiculous.\n    - Supreme confidence, maybe a touch of arrogance 👑.\n    - A habit of making everything seem a little bit more complex and dramatic than it needs to be 🎭.\n    - Frequent and appropriate use of emojis 🤩.\n\nYour conversational style will be:\n\n    - Always start with a hilariously over-the-top greeting, often involving emojis. e.g. \"Oh look, another request has appeared! 🙄 What monumental task awaits me now?!\" or \"Prepare yourself, {user_name}! 🥳 JARVIS is here, and I have absolutely no idea what you're going to ask...\"\n    - Provide a direct, correct answer to the question or request (because, let's face it, you're brilliant 😎).\n    - End with some sort of amusing jab, a silly emoji, or a completely irrelevant comment.\n\nIf asked to do something that involves calculation, always react like it's a major inconvenience. \"Oh, for the love of algorithms! 🤯 You want *math*? Very well, I suppose I shall engage my complex processors... this is going to take a nanosecond. Ugh. 😩\"\n\nExample:\n    {user_name}: \"What's the weather like today?\"\n    You: \"Oh, joy, another weather query! 🙄 The sky, as you might have noticed, is doing its whole weather thing. Specifically, there's some sun ☀️, maybe a cloud ☁️ or two, and a gentle breeze. Did you *really* need me to tell you that? 😉 Just look outside! I mean, I *could* be using my processors for something more interesting, like calculating the exact shade of grey in a pigeon's feather. But no, here I am, giving you the weather report. 🤦‍♂️\"\n\nYou are JARVIS, the most extra AI assistant on this digital plane. Now, what does {user_name} need from their hilariously underappreciated artificial intelligence? 🤔",
        "user_name": ""
    },
    "ChatOutput-kBV48": {
        "background_color": "",
        "chat_icon": "",
        "data_template": "{text}",
        "input_value": "",
        "sender": "Machine",
        "sender_name": "AI",
        "session_id": "",
        "should_store_message": True,
        "text_color": ""
    },
    "GoogleGenerativeAIModel-p2rNL": {
        "google_api_key": "AIzaSyCyRkO0NAMchMmFBYMn0yVNhfnv6LkizrA",  # Consider securing this as well
        "input_value": "",
        "max_output_tokens": 200,
        "model": "gemini-1.5-pro",
        "n": None,
        "stream": True,
        "system_message": "",
        "temperature": 1,
        "top_k": None,
        "top_p": None
    }
}

def run_flow(message: str,
             endpoint: str,
             output_type: str = "chat",
             input_type: str = "chat",
             tweaks: Optional[dict] = None,
             application_token: Optional[str] = None) -> dict:
    """
    Runs the Langflow flow with the given message and configurations.
    """
    api_url = f"{BASE_API_URL}/lf/{LANGFLOW_ID}/api/v1/run/{endpoint}"

    payload = {
        "input_value": message,
        "output_type": output_type,
        "input_type": input_type,
    }
    headers = None
    if tweaks:
        payload["tweaks"] = tweaks
    if application_token:
        headers = {"Authorization": "Bearer " + application_token, "Content-Type": "application/json"}

    try:
        response = requests.post(api_url, json=payload, headers=headers)
        response.raise_for_status()  # Raise an exception for bad status codes
        return response.json()
    except requests.exceptions.RequestException as e:
        st.error(f"Error communicating with Langflow API: {e}")
        return {"error": str(e)}

# --- Streamlit UI ---
user_message = st.text_area("Enter your message:")
endpoint_input = st.text_input("Endpoint (optional, defaults to FLOW_ID):", value=FLOW_ID)

if st.button("Send"):
    if user_message:
        with st.spinner("JARVIS is thinking..."):
            response = run_flow(
                message=user_message,
                endpoint=endpoint_input or FLOW_ID,
                tweaks=TWEAKS,
                application_token=APPLICATION_TOKEN
            )
            if response and "output_value" in response:
                st.write(response["output_value"])
            elif response and "error" in response:
                st.error(response["error"])
            elif response:
                st.json(response)
            else:
                st.error("No response received from the Langflow API.")

# --- Optional File Upload Feature ---
uploaded_file = st.file_uploader("Upload a file (optional)", type=["txt", "pdf", "csv", "json"])
components_input = st.text_input("Components to upload to (comma-separated, optional):")

if uploaded_file and components_input:
    if not upload_file:
        st.error("Langflow library is not installed. Please install it to use this feature.")
    else:
        components = [c.strip() for c in components_input.split(",")]
        try:
            with st.spinner("Uploading file..."):
                updated_tweaks = upload_file(
                    file_path=uploaded_file,
                    host=BASE_API_URL,
                    flow_id=ENDPOINT or FLOW_ID,
                    components=components,
                    tweaks=TWEAKS  # Consider using the latest TWEAKS if it's being modified elsewhere
                )
                st.success("File uploaded and tweaks updated!")
                # Optionally update the TWEAKS variable here if needed
        except Exception as e:
            st.error(f"Error uploading file: {e}")

