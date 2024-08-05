"""
This only currently contains ingredients relevant to the recipes.
We should add all ingredients
"""

import argparse
import logging
import sys
from datetime import datetime, timezone
from pathlib import Path

import pandas as pd
from sqlalchemy.orm import Session

from weird_salads.inventory.repository.models import (
    IngredientsModel,
    MenuModel,
    RecipeIngredientModel,
    StockModel,
)
from weird_salads.utils.unit_of_work import UnitOfWork
from weird_salads.utils.utils import generate_str_uuid

# from typing import List, Dict, Any

# Set up logging
logging.basicConfig(
    level=logging.DEBUG,
    format="%(levelname)s - %(message)s",
    handlers=[logging.StreamHandler(sys.stdout)],  # Send logs to stdout
)

logger = logging.getLogger(__name__)


def is_database_empty(session: Session) -> bool:
    """
    Check if the menu table in the database is empty.

    Parameters
    ----------
    session : Session
        The SQLAlchemy session used to query the database.

    Returns
    -------
    bool
        True if the menu table is empty, False otherwise.
    """
    return not session.query(MenuModel).first()


def validate_menu_data():
    # !TODO validate against a pydantic schema
    pass


def insert_menu_and_related_data(
    session: Session,
    menus_df: pd.DataFrame,
    recipes_df: pd.DataFrame,
    ingredients_df: pd.DataFrame,
    quant_to_inject: int,
) -> None:
    """
    Insert menu items, recipes, and ingredients into the database.


    Parameters
    ----------
    session : Session
        The SQLAlchemy session used to query the database.
    menus_df : pd.DataFrame
        DataFrame for menu items
    recipes_df : pd.DataFrame
        DataFrame for recipes
    ingredients_df : pd.DataFrame
        DataFrame for the ingredients table

    Notes
    -----
    This is achieved by:
    1. Iterating through `Menu` items
    2. For each Menu item inject `Ingredients` (if they do not exist)
    3. Inject into recipe_id, ingredient_id into `RecipeIngredients`
    """

    # !TODO validate against the schemas before injecting

    # Iterate through menu items
    for _, menu_row in menus_df.iterrows():
        recipe_id = menu_row["recipe_id"]

        # Get recipes for the current recipe_id
        recipe_rows = recipes_df[recipes_df["recipe_id"] == recipe_id]

        # Check if Menu already exists
        existing_menu = session.query(MenuModel).filter_by(id=recipe_id).first()
        if not existing_menu:
            # Insert Menu
            menu = MenuModel(
                id=int(recipe_id),
                name=recipe_rows["name"].iloc[0],  # get first example
                description=menu_row.get("description", ""),  # Optional field
                price=float(menu_row["price"]),
                created_on=datetime.now(timezone.utc),
                on_menu=True,
            )
            try:
                session.add(menu)
                session.commit()  # Commit after adding menu
            except Exception as e:
                logger.warning(f"Failed to add menu {recipe_id}: {e}")
                session.rollback()  # Rollback on failure

        # Insert menu_id-associated ingredients
        for _, recipe_row in recipe_rows.iterrows():
            ingredient_id = int(recipe_row["ingredient_id"])
            existing_ingredient = (
                session.query(IngredientsModel).filter_by(id=ingredient_id).first()
            )
            # try add if ingredient doesn't exist
            if not existing_ingredient:
                ingredient_data = ingredients_df[
                    ingredients_df["ingredient_id"] == ingredient_id
                ]

                if len(ingredient_data) != 1:
                    logger.warning(
                        f"Ingredient data not found or ambiguous for ID {ingredient_id}"
                    )
                    continue  # Skip this ingredient if data is not exactly one row

                ingredient_unit = ingredient_data.iloc[0]["unit"]
                ingredient_cost = ingredient_data.iloc[0]["cost"]

                ingredient = IngredientsModel(
                    id=int(ingredient_id),
                    name=str(ingredient_data.iloc[0]["name"]),
                    description="",
                )

                try:
                    session.add(ingredient)
                    session.commit()  # Commit after adding ingredient
                except Exception as e:
                    logger.warning(f"Failed to add ingredient {ingredient_id}: {e}")
                    session.rollback()  # Rollback on failure

                stock = StockModel(
                    id=generate_str_uuid(),
                    ingredient_id=int(ingredient_id),
                    unit=ingredient_unit,
                    quantity=quant_to_inject,
                    cost=ingredient_cost,
                    delivery_date=datetime.now(timezone.utc),
                    created_on=datetime.now(timezone.utc),
                )

                try:
                    session.add(stock)
                    session.commit()  # Commit after adding stock
                except Exception as e:
                    logger.warning(
                        f"Failed to add stock for ingredient {ingredient_id}: {e}"
                    )
                    session.rollback()  # Rollback on failure

            # Finaply insert into RecipeIngredients
            recipe_ingredient = RecipeIngredientModel(
                recipe_id=recipe_id,
                ingredient_id=ingredient_id,
                quantity=recipe_row["quantity"],
                unit=ingredient_unit,
            )
            try:
                session.add(recipe_ingredient)
                session.commit()  # Commit after adding recipe_ingredient
            except Exception as e:
                logger.warning(
                    f"Failed to add recipe ingredient for recipe {recipe_id} and ingredient {ingredient_id}: {e}"  # noqa: E501
                )
                session.rollback()  # Rollback on failure


def main(location_id: int, quantity: int, base_path: Path) -> None:
    logger.info("Starting data seeding process")

    with UnitOfWork() as uow:
        try:
            if is_database_empty(uow.session):
                # Load all data into DataFrames
                # locations_df = pd.read_csv('../data/locations.csv')
                menus_df = pd.read_csv(base_path / "menus.csv")
                recipes_df = pd.read_csv(base_path / "recipes.csv")
                ingredients_df = pd.read_csv(base_path / "ingredients.csv")

                # Filter menus by location_id
                if location_id not in menus_df["location_id"].values:
                    raise ValueError(
                        f"location_id {location_id} not found in menus data."
                    )

                filtered_menus_df = menus_df[
                    menus_df["location_id"] == location_id
                ].reset_index(drop=True)

                # Insert menus, recipes, and ingredients
                insert_menu_and_related_data(
                    uow.session, filtered_menus_df, recipes_df, ingredients_df, quantity
                )

                logger.info(
                    f"Seeding completed successfully for location {location_id}."
                )
            else:
                logger.info("Database already contains data. Skipping seeding.")
        except Exception as e:
            logger.error(f"An error occurred during seeding: {e}")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Data Seeding Script")
    parser.add_argument(
        "--location_id",
        type=int,
        required=True,
        help="The ID of the location to seed data for.",
    )
    parser.add_argument(
        "--quantity",
        type=int,
        default=0,
        help="The quantity of data to seed (in respective units).",
    )
    parser.add_argument(
        "--base_path",
        type=Path,
        default=Path("../../../../data"),
        help="The base path for data files.",
    )

    args = parser.parse_args()

    main(location_id=args.location_id, quantity=args.quantity, base_path=args.base_path)
