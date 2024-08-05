import pandas as pd
import requests
import streamlit as st

st.title("Streamlit App")

# Try to get a response from FastAPI
try:
    response = requests.get("http://fastapi:8000/order/")
    response.raise_for_status()  # Raise an HTTPError for bad responses (4xx and 5xx)
    data = response.json()

    # Extract orders from the response
    orders = data.get("orders", [])

    # Convert the list of orders to a DataFrame
    df = pd.DataFrame(orders)

    # Display the DataFrame as a table
    st.table(df)

except requests.exceptions.RequestException as e:
    st.write("Failed to connect to FastAPI:", e)
