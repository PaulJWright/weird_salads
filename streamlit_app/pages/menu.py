import pandas as pd
import requests
import streamlit as st


def fetch_menu_items():
    """
    GET menu items
    """
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


def place_order(item_id):
    """
    Place order, get order_id
    """
    try:
        response = requests.post(
            "http://fastapi:8000/order/", json={"menu_id": item_id}
        )
        response.raise_for_status()
        data = response.json()
        order_id = data.get("id", "unknown")
        return f"Success, your order number is {order_id}, don't forget it!"
    except requests.exceptions.HTTPError as http_err:
        if response.status_code == 400:
            # Handle specific client error (e.g., insufficient stock)
            error_mesage = response.json().get("detail", "Sorry, out of stock")
            if "InsufficientStockError" in error_mesage:
                return "Sorry, out of stock"
            return f"Order failed: {error_mesage}"
        return f"HTTP error occurred: {http_err}"
    except requests.exceptions.RequestException as e:
        st.write("Failed to place the order:", e)
        return "Failed to place the order."
    except Exception as e:
        st.write("An error occurred:", e)
        return "An error occurred while placing the order."


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

        for idx, row in df.iterrows():
            cols = st.columns([3, 1, 2])

            with cols[0]:
                st.write(f"{row['id']}. \t {row['name']} ({row['price']})")

            with cols[1]:
                button_key = f"order_{row['id']}"
                if st.button("Order", key=button_key):
                    # Place the order and get the response
                    st.session_state.order_status = place_order(row["id"])
                    st.session_state.current_order = row["name"]

            with cols[2]:
                if st.session_state.current_order == row["name"]:
                    st.write(f"Ordered: {row['name']}")
                    st.write(st.session_state.order_status)

    else:
        st.write("No menu items found.")


if __name__ == "__main__":
    display_menu()
