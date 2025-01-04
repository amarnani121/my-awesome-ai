import streamlit as st
import json
from langflow_model import run_flow

st.title("Langflow Streamlit Integration")
st.subheader("Interact with your Langflow Model")

# Get the application token from secrets
application_token = st.secrets["APPLICATION_TOKEN"]

user_input = st.text_input("Enter your message:", "")
if st.button("Submit"):
    if user_input.strip():
        with st.spinner("Processing..."):
            response = run_flow(message=user_input, application_token=application_token)
            st.success("Response Received!")
            st.json(response)
    else:
        st.warning("Please enter a message.")
