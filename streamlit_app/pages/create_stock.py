from datetime import datetime

import requests
import streamlit as st


def create_stock_item(payload):
    try:
        # Post data to FastAPI endpoint
        response = requests.post("http://fastapi:8000/inventory", json=payload)
        response.raise_for_status()
        return response.json(), None
    except requests.exceptions.RequestException as e:
        return None, str(e)


def add_stock_page():
    st.title("Add Stock Item")

    # Define the form for stock creation
    with st.form(key="add_stock_form"):
        st.header("Stock Information")

        # Input fields for stock data
        ingredient_id = st.number_input("Ingredient ID", min_value=1, step=1)
        stock_quantity = st.number_input(
            "Quantity", min_value=0.0, format="%.2f"
        )  # Float with 2 decimal places
        stock_unit = st.selectbox(
            "Unit", ["liter", "deciliter", "centiliter", "milliliter"]
        )  # Example units
        cost = st.number_input(
            "Cost per Unit", min_value=0.0, format="%.2f"
        )  # Float with 2 decimal places
        delivery_date = st.date_input(
            "Delivery Date", min_value=datetime(2000, 1, 1)
        )  # Date input

        # Create the stock data payload
        payload = {
            "stock": {
                "ingredient_id": ingredient_id,
                "unit": stock_unit,
                "quantity": stock_quantity,
                "cost": cost,
                "delivery_date": delivery_date.isoformat(),
                # Convert date to ISO format string
            }
        }

        # Submit button
        submit_button = st.form_submit_button(label="Add Stock")

        if submit_button:
            result, error = create_stock_item(payload)
            if error:
                st.error(f"Failed to add stock: {error}")
            else:
                st.success(f"Stock item added successfully: {result}")


if __name__ == "__main__":
    add_stock_page()
