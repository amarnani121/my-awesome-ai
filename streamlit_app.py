import streamlit as st
import requests
import os

# Get LangFlow credentials from environment variables (for security)
app_key = os.getenv('LANGFLOW_APP_KEY')  # Store in Streamlit Secrets or .env
api_key = os.getenv('LANGFLOW_API_KEY')  # Store in Streamlit Secrets or .env

# Function to get data from LangFlow API
def get_langflow_data(app_key, api_key, prompt):
    url = "https://api.langflow.com/endpoint"  # Replace with the correct endpoint
    headers = {
        "Authorization": f"Bearer {api_key}",
        "x-app-key": app_key
    }
    params = {
        "prompt": prompt
    }
    response = requests.post(url, headers=headers, json=params)
    return response.json()

# Streamlit app UI
st.title("LangFlow Streamlit Web App")

# User input for prompt
prompt = st.text_area("Enter your prompt:")

# Button to submit prompt
if st.button("Submit"):
    if prompt:
        result = get_langflow_data(app_key, api_key, prompt)
        if result:
            st.write("Response from LangFlow:")
            st.json(result)
        else:
            st.error("Error retrieving data from LangFlow.")
    else:
        st.warning("Please enter a prompt.")