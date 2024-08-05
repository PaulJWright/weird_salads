"""
Pydantic Schemas for API
"""

from datetime import datetime
from typing import List

from pydantic import BaseModel

# from typing_extensions import Annotated


# Orders-related Schema for the API
class CreateOrderSchema(BaseModel):
    menu_id: int

    class Config:
        extra = "forbid"


class GetOrderSchema(CreateOrderSchema):
    id: str  # changed to str (of UUID) to match how it is stored in SQLite
    created: datetime

    # price: Annotated[float, Field(ge=0.0, strict=True)]
    class Config:
        extra = "forbid"


class GetOrdersSchema(BaseModel):
    orders: List[GetOrderSchema]

    class Config:
        extra = "forbid"
