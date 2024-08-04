"""
Pydantic Schemas for API
"""

from datetime import datetime
from typing import List

from pydantic import BaseModel


# Orders-related Schema for the API
class CreateOrderSchema(BaseModel):
    menu_id: int

    class Config:
        extra = "forbid"


class GetOrderSchema(CreateOrderSchema):
    id: str  # changed to str (of UUID) to match how it is stored in SQLite
    created: datetime

    class Config:
        extra = "forbid"


class GetOrdersSchema(BaseModel):
    orders: List[GetOrderSchema]

    class Config:
        extra = "forbid"
