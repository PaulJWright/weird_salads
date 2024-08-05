from fastapi import FastAPI, HTTPException
from starlette import status

from weird_salads.api.schemas import (
    CreateOrderSchema,
    CreateStockSchema,
    GetMenuItemAvailabilitySchema,
    GetMenuItemSchema,
    GetOrderSchema,
    GetOrdersSchema,
    GetSimpleMenuSchema,
    GetStockItemSchema,
    GetStockSchema,
)
from weird_salads.inventory.inventory_service.exceptions import (
    IngredientNotFoundError,
    MenuItemNotFoundError,
    StockItemNotFoundError,
)
from weird_salads.inventory.inventory_service.inventory_service import MenuService
from weird_salads.inventory.repository.inventory_repository import MenuRepository
from weird_salads.orders.orders_service.orders_service import OrdersService
from weird_salads.orders.repository.orders_repository import OrdersRepository
from weird_salads.utils.unit_of_work import UnitOfWork

app = FastAPI()


# Menu
@app.get("/menu", response_model=GetSimpleMenuSchema, tags=["Menu"])
def get_menu():
    with UnitOfWork() as unit_of_work:
        repo = MenuRepository(unit_of_work.session)
        inventory_service = MenuService(repo)
        results = inventory_service.list_menu()
    return {"items": [result.dict() for result in results]}


@app.get("/menu/{item_id}", response_model=GetMenuItemSchema, tags=["Menu"])
def get_order(item_id: int):
    try:
        with UnitOfWork() as unit_of_work:
            repo = MenuRepository(unit_of_work.session)
            inventory_service = MenuService(repo)
            order = inventory_service.get_item(item_id=item_id)
        return order
    except MenuItemNotFoundError:
        raise HTTPException(
            status_code=404, detail=f"Menu Item with ID {item_id} not found"
        )


@app.get(
    "/menu/{item_id}/availability",
    response_model=GetMenuItemAvailabilitySchema,
    tags=["Menu"],
)
def get_availability(item_id: int):
    try:
        with UnitOfWork() as unit_of_work:
            repo = MenuRepository(unit_of_work.session)
            inventory_service = MenuService(repo)
            order = inventory_service.get_recipe_item_availability(item_id=item_id)
        return order  # Ensure `order` is an instance of `GetRecipeItemSchema`
    except MenuItemNotFoundError:
        raise HTTPException(
            status_code=404, detail=f"Menu Item with ID {item_id} not found"
        )


@app.get("/inventory", response_model=GetStockSchema, tags=["Inventory"])
def get_stock():
    with UnitOfWork() as unit_of_work:
        repo = MenuRepository(unit_of_work.session)
        inventory_service = MenuService(repo)
        results = inventory_service.list_stock()
    return {"items": [result.dict() for result in results]}


@app.get(
    "/inventory/stock/{stock_id}", response_model=GetStockItemSchema, tags=["Inventory"]
)
def get_stock_item(stock_id: str):
    try:
        with UnitOfWork() as unit_of_work:
            repo = MenuRepository(unit_of_work.session)
            inventory_service = MenuService(repo)
            order = inventory_service.get_stock_item(stock_id=stock_id)
        return order
    except StockItemNotFoundError:
        raise HTTPException(
            status_code=404, detail=f"Stock Item with ID {stock_id} not found"
        )


@app.get(
    "/inventory/ingredient/{ingredient_id}",
    response_model=GetStockSchema,
    tags=["Inventory"],
)
def get_ingredient(ingredient_id: int):
    try:
        with UnitOfWork() as unit_of_work:
            repo = MenuRepository(unit_of_work.session)
            inventory_service = MenuService(repo)
            ingredient = inventory_service.get_ingredient(ingredient_id=ingredient_id)
        return {"items": [record.dict() for record in ingredient]}
    except IngredientNotFoundError:
        raise HTTPException(
            status_code=404, detail=f"Ingredient Item with ID {ingredient_id} not found"
        )


@app.post(
    "/inventory",
    status_code=status.HTTP_201_CREATED,
    response_model=GetStockItemSchema,
    tags=["Inventory"],
)
def create_stock(payload: CreateStockSchema):
    with UnitOfWork() as unit_of_work:
        repo = MenuRepository(unit_of_work.session)
        stock_service = MenuService(repo)
        stock_item = payload.model_dump()["stock"]
        stock_item["unit"] = stock_item["unit"].value  # necessary?

        # Check if the ingredient exists
        ingredient = stock_service.get_ingredient(stock_item["ingredient_id"])
        if ingredient is None:
            raise HTTPException(
                status_code=404,
                detail=f"Ingredient with ID {stock_item['ingredient_id']} not found",
            )

        order = stock_service.ingest_stock(stock_item)
        unit_of_work.commit()
        return_payload = order.dict()
    return return_payload


# Orders
@app.get(
    "/order",
    response_model=GetOrdersSchema,
    tags=["Order"],
)
def get_orders():
    with UnitOfWork() as unit_of_work:
        repo = OrdersRepository(unit_of_work.session)
        orders_service = OrdersService(repo)
        results = orders_service.list_orders()
    return {"orders": [result.dict() for result in results]}


@app.post(
    "/order",
    status_code=status.HTTP_201_CREATED,
    response_model=GetOrderSchema,
    tags=["Order"],
)
def create_order(payload: CreateOrderSchema):
    with UnitOfWork() as unit_of_work:
        repo = OrdersRepository(unit_of_work.session)
        orders_service = OrdersService(repo)
        order = payload.model_dump()
        order = orders_service.place_order(order)
        unit_of_work.commit()  # this is when id and created are populated
        return_payload = order.dict()
    return return_payload
