import pandas as pd
import requests
import streamlit as st


def display_ingredient_items():
    st.title("Ingredient Items Report")

    ingredient_id = st.number_input("Enter Ingredient ID:", min_value=1, step=1)

    if st.button("Get Ingredient"):
        try:
            # Fetch ingredient data from the FastAPI endpoint
            response = requests.get(
                f"http://fastapi:8000/inventory/ingredient/{ingredient_id}"
            )
            response.raise_for_status()
            data = response.json()

            # Extract items from the response data
            ingredient_items = data.get("items", [])
            df_ingredient = pd.DataFrame(ingredient_items)

            # Check if the DataFrame is empty
            if df_ingredient.empty:
                st.write(f"No data found for Ingredient ID {ingredient_id}.")
            else:
                # Ensure 'delivery_date' is treated as a datetime object for sorting
                df_ingredient["delivery_date"] = pd.to_datetime(
                    df_ingredient["delivery_date"]
                )
                # Sort the DataFrame by 'delivery_date'
                df_ingredient_sorted = df_ingredient.sort_values(by="delivery_date")
                st.table(df_ingredient_sorted)

        except requests.exceptions.RequestException as e:
            st.write("Failed to connect to FastAPI:", e)


if __name__ == "__main__":
    display_ingredient_items()
