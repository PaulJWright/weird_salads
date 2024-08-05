"""
Services
"""

import requests
from fastapi import HTTPException

from weird_salads.api.schemas import UnitOfMeasure
from weird_salads.inventory.inventory_service.exceptions import InsufficientStockError
from weird_salads.orders.orders_service.exceptions import OrderNotFoundError
from weird_salads.orders.repository.orders_repository import OrdersRepository

__all__ = ["OrdersService"]


class OrdersService:
    def __init__(self, orders_repository: OrdersRepository):
        self.orders_repository = orders_repository

    def place_order(self, order_data):
        """
        Place an order after checking inventory and updating stock levels.
        """
        menu_id = int(order_data["menu_id"])

        # Fetch availability information for the menu item
        available_to_order, availability_response = self._get_menu_item_availability(
            menu_id
        )

        if not available_to_order:
            raise InsufficientStockError("Sorry, this is out of stock.")

        # Place the order, then deduct stock (uow deals with the committing later)
        order = self.orders_repository.add(order_data)

        for ingredient in availability_response["ingredient_availability"]:
            ingredient_id = int(ingredient["ingredient"]["id"])
            required_quantity = float(ingredient["required_quantity"])
            unit_string = str(ingredient["unit"])

            # Convert the unit string to the UnitOfMeasure Enum
            try:
                unit = UnitOfMeasure(unit_string)
            except ValueError:
                raise HTTPException(
                    status_code=400, detail=f"Invalid unit: {unit_string}"
                )
            self._update_stock(ingredient_id, -1 * required_quantity, unit)

        return order

    def get_order(self, order_id: str):
        """
        get single order
        """
        order = self.orders_repository.get(order_id)
        if order is not None:
            return order
        raise OrderNotFoundError(f"Order with id {order_id} not found")

    def list_orders(self):
        """
        get all orders
        """
        return self.orders_repository.list()

    def _get_menu_item_availability(self, menu_id: int):
        """
        Fetch availability details for the given menu item,
        including ingredient availability.
        """
        response = requests.get(f"http://localhost:8000/menu/{menu_id}/availability")
        if response.status_code == 200:
            availability = response.json()
            return availability["available_portions"] >= 0, response.json()
        else:
            raise HTTPException(
                status_code=response.status_code,
                detail=f"Failed to get availability for menu ID {menu_id}",
            )

    def _update_stock(
        self, ingredient_id: int, quantity: float, unit: UnitOfMeasure
    ) -> None:
        response = requests.post(
            "http://localhost:8000/inventory/update",
            json={
                "ingredient_id": ingredient_id,
                "quantity": quantity,
                "unit": unit.value,
            },
        )
        if response.status_code != 200:
            raise HTTPException(
                status_code=response.status_code,
                detail=f"Failed to update stock for Ingredient ID {ingredient_id}",
            )
