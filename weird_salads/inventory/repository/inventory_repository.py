"""
Building on a Repository Pattern
"""

from typing import Any, Dict

from sqlalchemy.orm import joinedload

from weird_salads.inventory.inventory_service.inventory import MenuItem, SimpleMenuItem
from weird_salads.inventory.repository.models import MenuModel, RecipeIngredientModel

__all__ = ["MenuRepository"]


class MenuRepository:
    def __init__(self, session):
        self.session = session

    def add(self):
        pass

    def _get(self, id):
        return (
            self.session.query(MenuModel).filter(MenuModel.id == str(id)).first()
        )  # noqa: E501

    def get(self, id):
        order = self._get(id)
        if order is not None:
            # do we want to return an instance of a SQLalchemy model?
            return SimpleMenuItem(**order.dict())

    def _get_tree(self, id):
        return (
            self.session.query(MenuModel)
            .options(
                joinedload(MenuModel.ingredients).joinedload(
                    RecipeIngredientModel.ingredient
                )
            )
            .filter(MenuModel.id == id)
            .first()
        )

    def get_tree(self, id: int) -> Dict[str, Any]:
        # Fetch the tree data
        tree = self._get_tree(id)

        # !TODO tidy this up, it's not elegant
        if tree is not None:
            # Prepare ingredients data as dictionaries for MenuItemIngredient instances
            ingredients = [
                {
                    "quantity": ri.quantity,
                    "unit": ri.unit,
                    "ingredient": {
                        "id": ri.ingredient.id,
                        "name": ri.ingredient.name,
                        "description": ri.ingredient.description or "",
                    },
                }
                for ri in tree.ingredients
            ]

            # Create a MenuItem instance
            menu_item = MenuItem(
                id=tree.id,
                name=tree.name,
                description=tree.description,
                price=tree.price,
                created_on=tree.created_on,
                on_menu=tree.on_menu,
                ingredients=ingredients,
            )

            # Convert MenuItem to a dictionary and return it
            return menu_item.dict()

    def list(self, limit=None):
        query = self.session.query(MenuModel)
        records = query.limit(limit).all()
        return [SimpleMenuItem(**record.dict()) for record in records]

    def update(self, id):
        pass

    def delete(self, id):
        pass
