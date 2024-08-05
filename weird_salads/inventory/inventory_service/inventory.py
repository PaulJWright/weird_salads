"""
Classes
"""

__all__ = ["SimpleMenuItem"]


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
