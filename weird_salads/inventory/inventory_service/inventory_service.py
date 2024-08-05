"""
Services
"""

from weird_salads.inventory.inventory_service.exceptions import MenuItemNotFoundError
from weird_salads.inventory.inventory_service.inventory import SimpleMenuItem
from weird_salads.inventory.repository.inventory_repository import MenuRepository

__all__ = ["MenuService"]


class MenuService:
    def __init__(self, menu_repository: MenuRepository):
        self.menu_repository = menu_repository

    def get(self, item_id):
        menu_item = self.menu_repository.get(item_id)
        if menu_item is not None:
            return menu_item
        raise MenuItemNotFoundError(f"Menu item with id {item_id} not found")

    def get_item(self, item_id: int) -> SimpleMenuItem:
        menu_item = self.menu_repository.get_tree(item_id)
        if menu_item is not None:
            return menu_item
        raise MenuItemNotFoundError(f"Menu item with id {item_id} not found")

    def list_menu(self):
        return self.menu_repository.list()
