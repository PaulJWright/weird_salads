"""
Building on a Repository Pattern
"""


from typing import List

from sqlalchemy.orm import joinedload

from weird_salads.inventory.inventory_service.inventory import (
    MenuItem,
    SimpleMenuItem,
    StockItem,
)
from weird_salads.inventory.repository.models import (
    MenuModel,
    RecipeIngredientModel,
    StockModel,
)

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

    def get_tree(self, id: int) -> MenuItem:
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
            return menu_item

    def list(self, limit=None):
        query = self.session.query(MenuModel)
        records = query.limit(limit).all()
        return [SimpleMenuItem(**record.dict()) for record in records]

    def update(self, id):
        pass

    def delete(self, id):
        pass

    # - Stock-related
    def _get_ingredient(self, ingredient_id: int):
        return (
            self.session.query(StockModel)
            .filter(StockModel.ingredient_id == int(ingredient_id))
            .all()
        )  # noqa: E501

    def get_ingredient(self, id: int) -> List[StockItem]:
        ingredients = self._get_ingredient(id)
        if ingredients:  # is not None:
            return [StockItem(**ingredient.dict()) for ingredient in ingredients]

    def _get_stock(self, id: str):
        return self.session.query(StockModel).filter(StockModel.id == id).first()

    def get_stock(self, id: str):
        order = self._get_stock(id)
        if order is not None:
            return StockItem(**order.dict())

    def list_stock(self, limit=None):  # need to implement limits
        query = self.session.query(StockModel)
        records = query.all()
        return [StockItem(**record.dict()) for record in records]
        # return [Ingredient(**record.dict()) for record in records]
        # should this return an IngredientItemsModel?

    def add_stock(self, item):
        print(item)
        record = StockModel(**item)
        self.session.add(record)
        return StockItem(**record.dict(), order_=record)

    def _convert_to_model(self, stock_item: StockItem) -> StockModel:
        return StockModel(
            id=stock_item.id,
            ingredient_id=stock_item.ingredient_id,
            unit=stock_item.unit,
            quantity=stock_item.quantity,
            cost=stock_item.cost,
            delivery_date=stock_item.delivery_date,
            created_on=stock_item.created_on,
        )

    def update_ingredient(self, stock_items: List[StockItem]) -> None:
        """
        Update stock items in the session.
        """
        merged_records = []
        for stock_item in stock_items:
            record = StockModel(**stock_item.dict())

            # Merge record with the session
            merged_records.append(self.session.merge(record))

        return merged_records
