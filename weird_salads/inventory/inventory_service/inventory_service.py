"""
Services
"""

from typing import Any, Dict, List

from weird_salads.api.schemas import UnitOfMeasure
from weird_salads.inventory.inventory_service.exceptions import (
    IngredientNotFoundError,
    MenuItemNotFoundError,
    StockItemNotFoundError,
)
from weird_salads.inventory.inventory_service.inventory import (
    MenuItem,
    MenuItemIngredient,
)
from weird_salads.inventory.repository.inventory_repository import MenuRepository

__all__ = ["MenuService", "UNIT_CONVERSIONS_TO_LITRE"]

# How many of unit in one litre
UNIT_CONVERSIONS_TO_LITRE = {
    UnitOfMeasure.liter: 1,
    UnitOfMeasure.deciliter: 10,
    UnitOfMeasure.centiliter: 100,
    UnitOfMeasure.milliliter: 1000,
}


class MenuService:
    def __init__(self, menu_repository: MenuRepository):
        self.menu_repository = menu_repository

    # for a simple representation
    def get(self, item_id):
        menu_item = self.menu_repository.get(item_id)
        if menu_item is not None:
            return menu_item
        raise MenuItemNotFoundError(f"Menu item with id {item_id} not found")

    def get_item(self, item_id: int) -> MenuItem:
        menu_item = self.menu_repository.get_tree(item_id)
        if menu_item is not None:
            return menu_item
        raise MenuItemNotFoundError(f"Menu item with id {item_id} not found")

    def list_menu(self):
        return self.menu_repository.list()

    # Fetch stock data for an ingredient
    def _fetch_stock_data(
        self, ingredient_id: int, required_unit: UnitOfMeasure
    ) -> float:
        """
        Fetch the stock data for an ingredient_id and convert to the required unit.
        """
        try:
            stock_items = self.get_ingredient(ingredient_id)
            total_quantity_in_required_unit = sum(
                self._convert_to_unit(item.quantity, item.unit, required_unit)
                for item in stock_items
            )
            return total_quantity_in_required_unit
        except Exception as e:
            print(f"Error fetching stock data: {e}")
            return 0

    # Convert quantity from one unit to another
    def _convert_to_unit(
        self, quantity: float, from_unit: UnitOfMeasure, to_unit: UnitOfMeasure
    ) -> float:
        if from_unit == to_unit:
            return quantity
        quantity_in_litres = quantity / UNIT_CONVERSIONS_TO_LITRE[from_unit]
        return quantity_in_litres * UNIT_CONVERSIONS_TO_LITRE[to_unit]

    # Calculate available portions based on recipe ingredients
    def _calculate_available_portions(
        self, recipe_ingredients: List[MenuItemIngredient]
    ) -> float:
        available_portions = float("inf")
        for ri in recipe_ingredients:
            ingredient_id = ri.ingredient.id
            required_quantity = ri.quantity
            required_unit = ri.unit
            try:
                # !TODO duplicated code
                total_quantity_in_stock = self._fetch_stock_data(
                    ingredient_id, required_unit
                )
                if required_quantity > 0:
                    portions_based_on_ingredient = (
                        total_quantity_in_stock // required_quantity
                    )
                    available_portions = min(
                        available_portions, portions_based_on_ingredient
                    )
            except Exception as e:
                print(f"Error processing ingredient ID {ingredient_id}: {e}")
                available_portions = 0
                break
        return available_portions

    # Get availability of a recipe item
    def get_recipe_item_availability(self, item_id: int) -> Dict[str, Any]:
        menu_item_with_ingredients = self.get_item(item_id)
        ingredients = menu_item_with_ingredients.ingredients

        ingredient_availability = [
            {
                "ingredient": {
                    "id": ri.ingredient.id,
                    "name": ri.ingredient.name,
                    "description": ri.ingredient.description,
                },
                "required_quantity": ri.quantity,
                "available_quantity": self._fetch_stock_data(ri.ingredient.id, ri.unit),
                "unit": ri.unit,
            }
            for ri in ingredients
        ]

        available_portions = self._calculate_available_portions(ingredients)

        return {
            "id": menu_item_with_ingredients.id,
            "name": menu_item_with_ingredients.name,
            "description": menu_item_with_ingredients.description or "",
            "price": menu_item_with_ingredients.price,
            "created_on": menu_item_with_ingredients.created_on,
            "on_menu": menu_item_with_ingredients.on_menu,
            "available_portions": int(available_portions),
            "ingredient_availability": ingredient_availability,
        }

    # - Stock-related
    # ---- ingredient_id queries
    def get_ingredient(self, ingredient_id: int):
        ingredient_item = self.menu_repository.get_ingredient(ingredient_id)
        if ingredient_item:
            return ingredient_item
        raise IngredientNotFoundError(f"items with id {ingredient_id} not found")  # fix

    def ingest_stock(self, item):
        return self.menu_repository.add_stock(item)

    # ---- stock_id queries
    def get_stock_item(self, stock_id: str):
        stock_item = self.menu_repository.get_stock(stock_id)
        if stock_item is not None:
            return stock_item
        raise StockItemNotFoundError(f"stock with id {stock_id} not found")  # fix

    def list_stock(self):  # needs options for filtering
        return self.menu_repository.list_stock()
