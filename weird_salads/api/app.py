from fastapi import FastAPI
from starlette import status

from weird_salads.api.schemas import CreateOrderSchema  # noqa
from weird_salads.api.schemas import GetOrderSchema, GetOrdersSchema
from weird_salads.orders.orders_service.orders_service import OrdersService
from weird_salads.orders.repository.orders_repository import OrdersRepository
from weird_salads.utils.unit_of_work import UnitOfWork

app = FastAPI()


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
