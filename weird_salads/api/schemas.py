"""
Pydantic Schemas for API
"""

from datetime import datetime
from typing import List
from uuid import UUID

from pydantic import BaseModel


# Orders-related Schema for the API
class CreateOrderSchema(BaseModel):
    menu_id: int

    class Config:
        extra = "forbid"


class GetOrderSchema(CreateOrderSchema):
    id: UUID  # should this be a string because SQLite?
    created: datetime

    class Config:
        extra = "forbid"


class GetOrdersSchema(BaseModel):
    orders: List[GetOrderSchema]

    class Config:
        extra = "forbid"
