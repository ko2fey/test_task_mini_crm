from fastapi import APIRouter, Depends, status, Query
from typing import Optional, Annotated

from schemas.schema_operator import CreateOperator
from schemas.schema_operator import UpdateOperator
from schemas.schema_operator import ResponseOperator
from schemas.schema_operator import ResponseListOperator
from schemas.schema_operator import FilterOperator
from schemas.schema_priority import ResponseListPriority
from schemas.schema_contact import ResponseListContact

from models import Operator

from services.service_operator import OperatorService
from services.service_contact import DistributeService

from dependencies.dependencies import get_service_operator
from dependencies.dependencies import get_filter_params_contact
from dependencies.dependencies import get_service_distribute

router = APIRouter(
    prefix="/operators",
    tags=["operators"],
)


@router.get("/", response_model=ResponseListOperator)
async def list_operators(
    service: Annotated[OperatorService, Depends(get_service_operator)],
    active: Optional[bool] = Query(None, description="Filter by active"),
):
    return service.repo.get_list(filter_params=FilterOperator(active=active))

@router.post(
    "/", 
    status_code=status.HTTP_201_CREATED, 
    response_model=ResponseOperator
)
async def create_operator(
    operator: CreateOperator,
    service: Annotated[OperatorService, Depends(get_service_operator)]
) -> Operator:
    return service.repo.create(
        operator.model_dump(exclude_unset=True, exclude_none=True)
    )

@router.put("/{id}", response_model=ResponseOperator)
async def update_operator(
    id: int,
    operator: UpdateOperator,
    service: Annotated[OperatorService, Depends(get_service_operator)]
) -> Operator:
    return service.repo.update(
        id, 
        operator.model_dump(exclude_unset=True, exclude_none=True)
    )

@router.delete(
    "/{id}",
    status_code=status.HTTP_204_NO_CONTENT,
    responses={
        status.HTTP_404_NOT_FOUND: {
            "description": "Operator not found",
            "content": {
                "application/json": {
                    "example": {
                        "detail": "Operator with id 123 not found"
                    }
                },
            },
        },
        status.HTTP_204_NO_CONTENT: {"description": "Operator successfully deleted"},
    }
)
async def delete_operator(
    id: int,
    service: Annotated[OperatorService, Depends(get_service_operator)]
) -> None:
        operator = service.repo.get(id)
        service.repo.delete(operator)

@router.get("/{id}/priorities", response_model=ResponseListPriority)
async def list_priorities(
    id: int,
    service: Annotated[OperatorService, Depends(get_service_operator)]
):
    return service.get_priorities(id)

@router.get(
    "/{id}/contacts",
    response_model=ResponseListContact)
async def list_contacts_by_operator(
    id: int,
    service: Annotated[DistributeService, Depends(get_service_distribute)],
    filter_params: FilterOperator = Depends(get_filter_params_contact),
):
    extended_filter_params = filter_params.model_copy(update={"operator_id": id})
    return service.repo.get_list(filter_params=extended_filter_params)