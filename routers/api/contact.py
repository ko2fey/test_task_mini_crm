from fastapi import APIRouter, Depends, status

from schemas.schema_contact import UpdateContact, ResponseContact
from schemas.schema_contact import ResponseListContact, FilterContact
from schemas.schema_lead import AssignLead

from models import Contact

from services.service_contact import DistributeService

from dependencies.dependencies import get_service_distribute
from dependencies.dependencies import get_filter_params_contact


router = APIRouter(
    prefix="/contacts",
    tags=["contacts"],
)
    
@router.get("/", response_model=ResponseListContact)
async def list_contacts(
    service: DistributeService = Depends(get_service_distribute),
    filter_params: FilterContact = Depends(get_filter_params_contact),
):
    return service.repo.get_list(
        filter_params=filter_params
    )

@router.post(
    "/",
    status_code=status.HTTP_201_CREATED, 
    response_model=ResponseContact
)
async def create_contact(
    data: AssignLead,
    service: DistributeService = Depends(get_service_distribute)
) -> Contact:
    return service.distribute_lead(data.model_dump(exclude_unset=True, exclude_none=True))

@router.put("/{id}", response_model=ResponseContact)
async def update_contacts(
    id: int,
    contact: UpdateContact,
    service: DistributeService = Depends(get_service_distribute)
) -> Contact:
    return service.repo.update(
        id, 
        contact.model_dump(exclude_unset=True, exclude_none=True)
    )

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
        source = service.repo.get(id)
        service.repo.delete(source)