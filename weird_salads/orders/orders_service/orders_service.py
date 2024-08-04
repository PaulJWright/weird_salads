"""
Services
"""

from weird_salads.orders.orders_service.exceptions import OrderNotFoundError
from weird_salads.orders.repository.orders_repository import OrdersRepository

__all__ = ["OrdersService"]


class OrdersService:
    def __init__(self, orders_repository: OrdersRepository):
        self.orders_repository = orders_repository

    def place_order(self, item):
        """
        place order
        """
        return self.orders_repository.add(item)

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
