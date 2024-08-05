"""
Pydantic Schemas for API
"""

from datetime import datetime, timezone
from typing import List, Optional

from pydantic import BaseModel, Field, field_validator
from typing_extensions import Annotated

# from typing_extensions import Annotated


# Menu-related Schema for the API
# Single Menu Item
class SimpleMenuItemSchema(BaseModel):
    name: str
    description: Optional[str] = None
    price: Annotated[float, Field(ge=0.0, strict=True)]
    created_on: datetime = datetime.now(timezone.utc)
    on_menu: bool = True

    class Config:
        extra = "forbid"

    @field_validator("price")
    def quantity_non_nullable(cls, value):
        assert value is not None, "price may not be None"
        return value


# GET, now includes id...
class GetMenuItemSchema(SimpleMenuItemSchema):
    id: int


# GET Menu (list of Menu items)
class GetMenuSchema(BaseModel):
    items: List[GetMenuItemSchema]


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
