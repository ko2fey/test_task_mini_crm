from fastapi import APIRouter, Depends, status
from schemas.schema_operator import CreateOperator, UpdateOperator, ResponseOperator
from schemas.schema_operator import ResponseListOperator, FilterOperator
from schemas.schema_priority import ResponseListPriority
from schemas.schema_contact import ResponseListContact

from models import Operator

from services.service_operator import OperatorService

from dependencies import get_service_operator
from dependencies import get_service_priority

router = APIRouter(
    prefix="/operators",
    tags=["operators"],
)


@router.get("/", response_model=ResponseListOperator)
async def list_operators(
    service: OperatorService = Depends(get_service_operator)
):
    return service.repo.get_list()

@router.post(
    "/", 
    status_code=status.HTTP_201_CREATED, 
    response_model=ResponseOperator
)
async def create_operator(
    operator: CreateOperator,
    service: OperatorService = Depends(get_service_operator)
) -> Operator:
    return service.repo.create(operator)

@router.put("/{id}", response_model=ResponseOperator)
async def update_operator(
    id: int,
    operator: UpdateOperator,
    service: OperatorService = Depends(get_service_operator)
) -> Operator:
    return service.repo.update(id, operator)

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
    service: OperatorService = Depends(get_service_operator)
) -> None:
        operator = service.repo.get(id)
        service.repo.delete(operator)

@router.get("/{id}/priorities", response_model=ResponseListPriority)
async def list_priorities(
    id: int,
    service: OperatorService = Depends(get_service_operator)
):
    return service.get_priorities(id)

@router.get("/{id}/contacts", response_model=ResponseListContact)
async def list_contacts_by_operator(
    id: int,
    service: OperatorService = Depends(get_service_operator)
):
    return service.get_contacts(id)