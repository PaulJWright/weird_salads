import pandas as pd
import requests
import streamlit as st


def display_order_report():
    st.title("Report: Orders")

    try:
        response = requests.get("http://fastapi:8000/order/")
        response.raise_for_status()
        data = response.json()

        orders = data.get("orders", [])
        df = pd.DataFrame(orders)

        if df.empty:  # Check if the DataFrame is empty
            st.write("No data.")
        else:
            st.table(df)

    except requests.exceptions.RequestException as e:
        st.write("Failed to connect to FastAPI:", e)


if __name__ == "__main__":
    display_order_report()
