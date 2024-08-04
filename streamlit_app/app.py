import requests
import streamlit as st

st.title("Streamlit App")

# Try to get a response from FastAPI
try:
    response = requests.get("http://fastapi:8000")
    response.raise_for_status()  # Raise an HTTPError for bad responses (4xx and 5xx)
    data = response.json()

    st.write("Response:", data)

except requests.exceptions.RequestException as e:
    st.write("Failed to connect to FastAPI:", e)
