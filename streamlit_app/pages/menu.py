import pandas as pd
import requests
import streamlit as st


def display_menu():
    st.header("Menu")

    try:
        # Fetch data from FastAPI
        response = requests.get("http://fastapi:8000/menu/")
        response.raise_for_status()
        data = response.json()

        menu_items = data.get("items", [])
        df = pd.DataFrame(menu_items)

        df = df[df["on_menu"]]  # filter on_menu == True

        df = df[["name", "price"]]
        df["price"] = df["price"].apply(lambda x: f"{x:.2f}")

        if df.empty:  # Check if the DataFrame is empty
            st.write("No data.")
        else:
            st.table(df)

    except requests.exceptions.RequestException as e:
        st.write("Failed to connect to FastAPI:", e)
    except Exception as e:
        st.write("An error occurred:", e)


if __name__ == "__main__":
    display_menu()
