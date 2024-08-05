import pandas as pd
import requests
import streamlit as st


def fetch_menu_items():
    try:
        response = requests.get("http://fastapi:8000/menu/")
        response.raise_for_status()
        data = response.json()
        return data.get("items", [])
    except requests.exceptions.RequestException as e:
        st.write("Failed to connect to FastAPI:", e)
        return []
    except Exception as e:
        st.write("An error occurred:", e)
        return []


def display_menu():
    st.header("Menu")

    menu_items = fetch_menu_items()

    # Initialize session state for tracking the currently ordered item
    if "current_order" not in st.session_state:
        st.session_state.current_order = None

    if menu_items:
        # Create a DataFrame to display menu items
        df = pd.DataFrame(menu_items)

        # Filter out items that are not on the menu
        df = df[df["on_menu"]]
        df["price"] = df["price"].apply(lambda x: f"${x:.2f}")

        st.write("### Menu Items")

        for idx, row in df.iterrows():
            cols = st.columns([3, 1, 2])

            with cols[0]:
                st.write(f"{row['name']} ({row['price']})")

            with cols[1]:
                # Use a unique key for each button
                button_key = f"order_{row['id']}"
                if st.button("Order", key=button_key):
                    st.session_state.current_order = row["name"]

            with cols[2]:
                # Display the order status if it matches the current order
                if st.session_state.current_order == row["name"]:
                    st.write(f"Ordered: {row['name']}")

    else:
        st.write("No menu items found.")


if __name__ == "__main__":
    display_menu()
