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


def fetch_recipe(item_id):
    try:
        response = requests.get(f"http://fastapi:8000/menu/{item_id}")
        response.raise_for_status()
        return response.json()
    except requests.exceptions.RequestException as e:
        st.write("Failed to connect to FastAPI:", e)
        return {}
    except Exception as e:
        st.write("An error occurred:", e)
        return {}


def display_menu():
    st.header("Menu")

    menu_items = fetch_menu_items()
    if menu_items:
        # Create a DataFrame to display menu items
        df = pd.DataFrame(menu_items)

        # Filter out items that are not on the menu
        df = df[df["on_menu"]]  # filter on_menu == True
        df = df[["id", "name", "price"]]
        df["price"] = df["price"].apply(lambda x: f"${x:.2f}")

        if df.empty:
            st.write("No data.")
        else:
            # Create a table for menu items
            st.write("### Menu Items")
            for idx, row in df.iterrows():
                item_id = row["id"]
                item_name = row["name"]
                item_price = row["price"]

                # Display item details and order button
                col1, col2 = st.columns([4, 1])
                with col1:
                    st.write(f"**{item_name}** ({item_price})")
                with col2:
                    if st.button("Order", key=f"order_{item_id}"):
                        st.write(f"Ordered: {item_name}")

            # Optionally add a section for ingredients
            st.write("### Ingredients")
            selected_item_id = st.selectbox(
                "Select an item to view ingredients", df["id"]
            )
            if selected_item_id:
                recipe = fetch_recipe(selected_item_id)
                if recipe:
                    ingredients_df = pd.DataFrame(recipe.get("ingredients", []))
                    if not ingredients_df.empty:
                        # Expand ingredient details
                        ingredients_df["ingredient_name"] = ingredients_df[
                            "ingredient"
                        ].apply(lambda x: x["name"])
                        ingredients_df["ingredient_id"] = ingredients_df[
                            "ingredient"
                        ].apply(lambda x: x["id"])
                        ingredients_df = ingredients_df[
                            ["ingredient_name", "quantity", "unit"]
                        ]
                        ingredients_df.columns = ["Ingredient", "Quantity", "Unit"]

                        st.table(ingredients_df)
                    else:
                        st.write("No ingredients available.")
                else:
                    st.write("No details available.")
    else:
        st.write("No menu items found.")


if __name__ == "__main__":
    display_menu()
