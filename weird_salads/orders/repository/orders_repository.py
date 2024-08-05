"""
Building on a Repository Pattern
"""

from weird_salads.orders.orders_service.orders import Order
from weird_salads.orders.repository.models import OrderModel

__all__ = ["OrdersRepository"]


class OrdersRepository:
    def __init__(self, session):
        self.session = session

    def add(self, item):
        record = OrderModel(**item)
        self.session.add(record)
        return Order(**record.dict(), order_=record)

    def _get(self, id: str):
        return (
            self.session.query(OrderModel).filter(OrderModel.id == id).first()
        )  # noqa: E501

    def get(self, id):
        order = self._get(id)
        if order is not None:
            return Order(**order.dict())

    def list(self):
        query = self.session.query(OrderModel)
        records = query.all()
        return [Order(**record.dict()) for record in records]

    def delete(self, id):
        pass
