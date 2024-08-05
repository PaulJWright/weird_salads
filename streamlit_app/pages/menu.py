import pandas as pd
import requests
import streamlit as st


# Function to fetch menu items
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


# Function to fetch availability of a specific menu item
def fetch_item_availability(item_id):
    try:
        response = requests.get(
            f"http://fastapi:8000/menu/{item_id}/availability"
        )  # Update endpoint if necessary
        response.raise_for_status()
        return response.json()
    except requests.exceptions.RequestException as e:
        st.write("Failed to connect to FastAPI:", e)
        return None
    except Exception as e:
        st.write("An error occurred:", e)
        return None


# Function to display menu items
def display_menu():
    st.header("Menu")

    menu_items = fetch_menu_items()

    # Initialize session state for tracking the current order and status
    if "current_order" not in st.session_state:
        st.session_state.current_order = None
        st.session_state.order_status = ""

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
                button_key = f"order_{row['id']}"
                if st.button("Order", key=button_key):
                    # Fetch availability when button is clicked
                    availability = fetch_item_availability(row["id"])
                    if availability and availability.get("available_portions", 0) >= 1:
                        st.session_state.current_order = row["name"]
                        st.session_state.order_status = "Order success!"
                    else:
                        st.session_state.order_status = "Sorry, that's out of stock"

            with cols[2]:
                if st.session_state.current_order == row["name"]:
                    st.write(f"Ordered: {row['name']}")
                    st.write(st.session_state.order_status)

    else:
        st.write("No menu items found.")


if __name__ == "__main__":
    display_menu()
