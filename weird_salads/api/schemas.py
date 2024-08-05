"""
Pydantic Schemas for API
"""

from datetime import datetime, timezone
from enum import Enum
from typing import List, Optional

from pydantic import BaseModel, Field, field_validator
from typing_extensions import Annotated

# from typing_extensions import Annotated


# =================================
# Menu-related Schema for the API
# =================================
class UnitOfMeasure(str, Enum):
    """
    Enum for units of measure
    """

    liter = "liter"
    deciliter = "deciliter"
    centiliter = "centiliter"
    milliliter = "milliliter"


class SimpleMenuItemSchema(BaseModel):
    """
    Simple Menu Item (an overview).
    """

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
class GetSimpleMenuItemSchema(SimpleMenuItemSchema):
    id: int


# GET Menu (list of Menu items)
class GetSimpleMenuSchema(BaseModel):
    """
    Menu (GET)
    """

    items: List[GetSimpleMenuItemSchema]

    class Config:
        extra = "forbid"


# Ingredient-related things
# -------------------------


# Schema for IngredientItem
class IngredientItemSchema(BaseModel):
    name: str
    description: Optional[str] = None

    class Config:
        extra = "forbid"


class GetIngredientItemSchema(IngredientItemSchema):
    id: int

    class Config:
        extra = "forbid"


# Schema for MenuItemIngredient
class MenuItemIngredientSchema(BaseModel):
    quantity: float
    unit: UnitOfMeasure
    ingredient: GetIngredientItemSchema

    class Config:
        extra = "forbid"


# GET, now includes id and ingredients...
class GetMenuItemSchema(GetSimpleMenuItemSchema):
    """
    Menu Item detail (GET)
    """

    id: int
    ingredients: List[
        MenuItemIngredientSchema
    ]  # Include ingredients with the menu item


# =================================
# Orders-related Schema for the API
# =================================
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
