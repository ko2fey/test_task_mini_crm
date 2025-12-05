from fastapi import APIRouter, Depends, status
from schemas.schema_contact import CreateContact, UpdateContact, ResponseContact
from schemas.schema_contact import ResponseListContact
from schemas.schema_lead import AssignLead

from models import Contact

from services.service_contact import DistributeService

from dependencies import get_service_distribute

router = APIRouter(
    prefix="/contacts",
    tags=["contacts"],
)

# Создать ИСТОЧНИК
@router.get("/", response_model=ResponseListContact)
async def list_sources(
    service: DistributeService = Depends(get_service_distribute)
):
    return service.repo_distribute.get_list()

@router.post(
    "/",
    status_code=status.HTTP_201_CREATED, 
    response_model=ResponseContact
)
async def create_contact(
    data: AssignLead,
    service: DistributeService = Depends(get_service_distribute)
) -> Contact:
    return service.distrebute_lead(data)

@router.put("/{id}", response_model=ResponseContact)
async def update_operator(
    id: int,
    contact: UpdateContact,
    service: DistributeService = Depends(get_service_distribute)
) -> Contact:
    return service.repo_distribute.update(id, contact)

@router.delete(
    "/{id}",
    status_code=status.HTTP_204_NO_CONTENT,
    responses={
        status.HTTP_404_NOT_FOUND: {
            "description": "Contact not found",
            "content": {
                "application/json": {
                    "example": {
                        "detail": "Contact with id 123 not found"
                    }
                },
            },
        },
        status.HTTP_204_NO_CONTENT: {"description": "Contact successfully deleted"},
    }
)
async def delete_operator(
    id: int,
    service: DistributeService = Depends(get_service_distribute)
) -> None:
        source = service.repo_distribute.get(id)
        service.repo_distribute.delete(source)