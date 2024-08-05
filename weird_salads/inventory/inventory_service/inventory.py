"""
Classes
"""

__all__ = [
    "SimpleMenuItem",
    "MenuItem",
    "MenuItemIngredient",
    "IngredientItem",
    "StockItem",
]


# - MenuItem holds MenuItemIngredients
# - SimpleMenuItem <- a simplified version of MenuItem sans ingredients
# - MenuAvailabilityItem <- more complex MenuItem with availability info
class SimpleMenuItem:
    def __init__(self, id, name, description, price, created_on, on_menu):
        self.name = name
        self.id = id
        self.description = description
        self.price = price
        self.created_on = created_on
        self.on_menu = on_menu

    def dict(self):
        return {
            "id": self.id,
            "name": self.name,
            "description": self.description,
            "price": self.price,
            "created_on": self.created_on,
            "on_menu": self.on_menu,
        }


# RecipeItem holds a set of RecipeIngredient objects
class MenuItem:
    def __init__(
        self, id, name, description, price, created_on, on_menu, ingredients=None
    ):
        self.id = id
        self.name = name
        self.description = description
        self.price = price
        self.created_on = created_on
        self.on_menu = on_menu
        # Initialize ingredients as MenuItemIngredient instances from dictionaries
        self.ingredients = [MenuItemIngredient(**item) for item in (ingredients or [])]

    def dict(self):
        result = {
            "id": self.id,
            "name": self.name,
            "description": self.description,
            "price": self.price,
            "created_on": self.created_on.isoformat() if self.created_on else None,
            "on_menu": self.on_menu,
            "ingredients": [ingredient.dict() for ingredient in self.ingredients],
        }
        return result


class MenuItemIngredient:
    def __init__(self, quantity, unit, ingredient=None):
        self.quantity = quantity
        self.unit = unit
        # Initialize ingredient as IngredientItem from dictionary
        self.ingredient = IngredientItem(**(ingredient or {}))

    def dict(self):
        result = {
            "quantity": self.quantity,
            "unit": self.unit,
            "ingredient": self.ingredient.dict() if self.ingredient else None,
        }
        return result


class IngredientItem:
    def __init__(self, id, name, description):
        self.id = id
        self.name = name
        self.description = description

    def dict(self):
        result = {
            "id": self.id,
            "name": self.name,
            "description": self.description,
        }
        return result


class StockItem:
    def __init__(
        self,
        id,
        ingredient_id,
        unit,
        quantity,
        cost,
        delivery_date,
        created_on,
        order_=None,
    ):
        self._order = order_
        self._id = id
        self.ingredient_id = ingredient_id
        self.unit = unit
        self.quantity = quantity
        self.cost = cost
        self.delivery_date = delivery_date
        self.created_on = created_on

    @property
    def id(self):
        return self._id or self._order.id

    def dict(self):
        return {
            "id": self.id,
            "ingredient_id": self.ingredient_id,
            "unit": self.unit,
            "quantity": self.quantity,
            "cost": self.cost,
            "delivery_date": self.delivery_date,
            "created_on": self.created_on,
        }
