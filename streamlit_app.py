import streamlit as st
import requests

# Application token
APPLICATION_TOKEN = "AstraCS:asQDxBwpZtXPrurvqluzffPO:da9113aafcfc71137ed7d3dd5d073a081bf21be42c3d7ee49801d760d82508e4"

# API base URL
API_BASE_URL = "https://your-langflow-api-endpoint"  # Replace with your LangFlow API endpoint

# Streamlit App
st.title("LangFlow API Integration")

# User input
st.write("Enter a query to interact with your LangFlow application:")
user_query = st.text_input("Query:")

# Submit button
if st.button("Submit"):
    if user_query.strip():
        # Prepare the request headers and payload
        headers = {
            "Authorization": f"Bearer {APPLICATION_TOKEN}",
            "Content-Type": "application/json",
        }
        payload = {"query": user_query}

        try:
            # Send the POST request
            response = requests.post(f"{API_BASE_URL}/endpoint-path", json=payload, headers=headers)
            
            # Handle the response
            if response.status_code == 200:
                response_data = response.json()
                st.success(f"Response: {response_data}")
            else:
                st.error(f"Error {response.status_code}: {response.text}")
        except requests.exceptions.RequestException as e:
            st.error(f"An error occurred: {e}")
    else:
        st.warning("Please enter a valid query.")

