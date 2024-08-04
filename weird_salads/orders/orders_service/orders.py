"""
Classes
"""
__all__ = ["Order"]


class Order:
    def __init__(self, id, created, menu_id, order_=None):
        self._order = order_  # what is the use of order_
        self._id = id
        self._created = created
        self.menu_id = menu_id

    @property
    def id(self):
        return self._id or self._order.id

    @property
    def created(self):
        return self._created or self._order.created

    def dict(self):
        return {
            "id": self.id,
            "menu_id": self.menu_id,
            "created": self.created,
        }
