import pandas as pd
import requests
import streamlit as st


def display_stock_items():
    st.title("Report: Stock")

    try:
        # Fetch stock data from the FastAPI endpoint
        response = requests.get("http://fastapi:8000/inventory/")
        response.raise_for_status()
        data = response.json()

        # Extract items from the response data
        stock_items = data.get("items", [])
        df_stock = pd.DataFrame(stock_items)

        # Check if the DataFrame is empty
        if df_stock.empty:
            st.write("No stock data available.")
        else:
            st.table(df_stock)

    except requests.exceptions.RequestException as e:
        st.write("Failed to connect to FastAPI:", e)


if __name__ == "__main__":
    display_stock_items()
