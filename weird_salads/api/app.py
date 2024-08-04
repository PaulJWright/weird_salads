from fastapi import FastAPI

from weird_salads.api.schemas import GetOrdersSchema
from weird_salads.orders.orders_service.orders_service import OrdersService
from weird_salads.orders.repository.orders_repository import OrdersRepository
from weird_salads.utils.unit_of_work import UnitOfWork

app = FastAPI()


@app.get("/order", response_model=GetOrdersSchema, tags=["Order"])
def get_orders():
    with UnitOfWork() as unit_of_work:
        repo = OrdersRepository(unit_of_work.session)
        orders_service = OrdersService(repo)
        results = orders_service.list_orders()
    return {"orders": [result.dict() for result in results]}
