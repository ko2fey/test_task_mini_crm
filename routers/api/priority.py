from fastapi import APIRouter, Depends, status
from schemas.schema_priority import CreatePriority, ResponsePriority
from schemas.schema_priority import ResponseListPriority, UpdatePriority

from models import OperatorSourcePriority

from services.service_priority import PriorityService

from dependencies.dependencies import get_service_priority

router = APIRouter(
    prefix="/priorities",
    tags=["priorities"],
)

@router.get("/", response_model=ResponseListPriority)
async def list_priorities(
    service: PriorityService = Depends(get_service_priority)
):
    return service.repo.get_list()


@router.post(
    "/",
    status_code=status.HTTP_201_CREATED,
    response_model=ResponsePriority
)
async def create_priority(
    data: CreatePriority,
    service: PriorityService = Depends(get_service_priority)
) -> OperatorSourcePriority:
    new_priority = service.assign_priority(
        data.model_dump(exclude_unset=True, exclude_none=True)
    )
    return new_priority

@router.put("/{id}", response_model=ResponsePriority)
async def update_priority(
    id: int,
    priority: UpdatePriority,
    service: PriorityService = Depends(get_service_priority)
) -> OperatorSourcePriority:
    return service.repo.update(
        id, 
        priority.model_dump(exclude_unset=True, exclude_none=True)
    )