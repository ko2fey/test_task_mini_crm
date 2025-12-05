from fastapi import APIRouter, Depends, status
from schemas.schema_operator import CreateOperator, UpdateOperator, ResponseOperator
from schemas.schema_operator import ResponseListOperator, FilterOperator
from schemas.schema_priority import CreatePriority, ResponsePriority, ResponseListPriority

from models import Operator, OperatorSourcePriority

from services.service_operator import OperatorService
from services.service_priority import PriorityService

from dependencies import get_service_operator
from dependencies import get_service_priority

router = APIRouter(
    prefix="/priorities",
    tags=["priorities"],
)

@router.get("/", response_model=ResponseListPriority)
async def list_priorities(
    service: PriorityService = Depends(get_service_priority)
):
    return service.repo_priority.get_list()


@router.post(
    "/",
    status_code=status.HTTP_201_CREATED,
    response_model=ResponsePriority
)
async def create_priority(
    data: CreatePriority,
    service: PriorityService = Depends(get_service_priority)
) -> OperatorSourcePriority:
    new_priority = service.assign_priority(data)
    return new_priority