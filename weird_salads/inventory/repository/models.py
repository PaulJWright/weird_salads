"""
SQLalchemy Models
"""

from datetime import datetime, timezone
from enum import Enum

from sqlalchemy import Boolean, CheckConstraint, Column, DateTime
from sqlalchemy import Enum as SQLAEnum
from sqlalchemy import Float, ForeignKey, Index, Integer, String
from sqlalchemy.orm import relationship

from weird_salads.utils.sqlalchemy_base import Base
from weird_salads.utils.utils import generate_str_uuid

__all__ = [
    "UnitOfMeasure",
    "MenuModel",
    "IngredientsModel",
    "RecipeIngredientModel",
    "StockModel",
]


class UnitOfMeasure(Enum):
    liter = "liter"
    deciliter = "deciliter"
    centiliter = "centiliter"
    milliliter = "milliliter"


class MenuModel(Base):
    __tablename__ = "menu"

    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False)
    description = Column(String, nullable=True)
    price = Column(Float, nullable=False)
    created_on = Column(DateTime, default=datetime.now(timezone.utc))
    on_menu = Column(Boolean, default=True)

    # is this why you can use "on_orm" ?
    def dict(self):
        return {
            "id": self.id,
            "name": self.name,
            "description": self.description,
            "price": self.price,
            "created_on": self.created_on,
            "on_menu": self.on_menu,
        }

    __table_args__ = (CheckConstraint("price >= 0.0", name="check_price_non_negative"),)

    # Define relationship to RecipeIngredient
    ingredients = relationship("RecipeIngredientModel", back_populates="recipe")


class IngredientsModel(Base):
    __tablename__ = "ingredients"

    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False, unique=True)
    description = Column(String, nullable=True)
    # standard_unit = Column(SQLAEnum(UnitOfMeasure), nullable=False)
    # -- assume everything is in volume so not required
    # cost = Column(Float, nullable=False) # this needs to come from the stock

    # Define relationship to RecipeIngredient
    recipe_ingredients = relationship(
        "RecipeIngredientModel", back_populates="ingredient"
    )
    stock_entries = relationship("StockModel", back_populates="ingredient")

    def dict(self):
        return {
            "id": self.id,
            "name": self.name,
            "description": self.description,
        }


class RecipeIngredientModel(Base):
    __tablename__ = "recipe_ingredients"

    recipe_id = Column(Integer, ForeignKey("menu.id"), primary_key=True)
    ingredient_id = Column(Integer, ForeignKey("ingredients.id"), primary_key=True)
    quantity = Column(Float, nullable=False)
    unit = Column(SQLAEnum(UnitOfMeasure), nullable=False)
    # unit = Column(String, nullable=False)

    __table_args__ = (
        CheckConstraint("quantity >= 0.0", name="check_quantity_non_negative"),
        Index(
            "idx_recipe_ingredient", "recipe_id", "ingredient_id"
        ),  # Composite index on recipe_id and ingredient_id
    )

    # Define relationships with back_populates
    recipe = relationship("MenuModel", back_populates="ingredients")
    ingredient = relationship("IngredientsModel", back_populates="recipe_ingredients")

    def dict(self):
        return {
            "recipe_id": self.recipe_id,
            "ingredient_id": self.ingredient_id,
            "quantity": self.quantity,
            "unit": self.unit,
        }


class StockModel(Base):
    __tablename__ = "stock"

    id = Column(String, primary_key=True, default=generate_str_uuid)
    ingredient_id = Column(Integer, ForeignKey("ingredients.id"))
    unit = Column(SQLAEnum(UnitOfMeasure), nullable=False)  # this might actually work
    # unit = Column(String, nullable=False)
    quantity = Column(Float, nullable=False)
    cost = Column(Float, nullable=False)
    # expiry_date = Column(DateTime, nullable=False) # !TODO ?
    delivery_date = Column(DateTime, default=datetime.now(timezone.utc))
    created_on = Column(DateTime, default=datetime.now(timezone.utc))

    __table_args__ = (
        CheckConstraint("quantity >= 0.0", name="check_quantity_non_negative"),
        CheckConstraint("cost >= 0.0", name="check_cost_non_negative"),
        Index("idx_stock_ingredient", "ingredient_id"),
        Index("idx_stock_delivery_date", "delivery_date"),
    )

    # Define relationship with Ingredient
    ingredient = relationship("IngredientsModel", back_populates="stock_entries")

    def dict(self):
        return {
            "id": self.id,
            "ingredient_id": self.ingredient_id,
            "unit": self.unit,
            "quantity": self.quantity,
            "cost": self.cost,
            "delivery_date": self.delivery_date,
            "created_on": self.created_on,
        }
