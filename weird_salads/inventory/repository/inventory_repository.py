"""
Building on a Repository Pattern
"""

from weird_salads.inventory.inventory_service.inventory import SimpleMenuItem
from weird_salads.inventory.repository.models import MenuModel

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

    def list(self, limit=None):
        query = self.session.query(MenuModel)
        records = query.limit(limit).all()
        return [SimpleMenuItem(**record.dict()) for record in records]

    def update(self, id):
        pass

    def delete(self, id):
        pass
