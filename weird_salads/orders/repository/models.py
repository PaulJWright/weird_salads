"""
SQLalchemy Models
"""

from datetime import datetime, timezone

from sqlalchemy import Column, DateTime, Integer, String

from weird_salads.utils.sqlalchemy_base import Base
from weird_salads.utils.utils import generate_str_uuid

__all__ = ["OrderModel"]


class OrderModel(Base):
    __tablename__ = "order"

    id = Column(String, primary_key=True, default=generate_str_uuid)
    menu_id = Column(Integer, nullable=False)  # this will end up being a ForeignKey
    created = Column(DateTime, default=datetime.now(timezone.utc))

    def dict(self):
        return {
            "id": self.id,
            "menu_id": self.menu_id,
            "created": self.created,
        }
