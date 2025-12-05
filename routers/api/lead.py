from schemas.schema_lead import ResponseLead, ResponseListLead, CreateLead, UpdateLead
from schemas.schema_contact import ResponseListContact
from fastapi import APIRouter, Depends, status
from models import Lead
from services.service_lead import LeadService
from dependencies import get_service_lead

router = APIRouter(
    prefix="/leads",
    tags=["leads"],
)


@router.get("/", response_model=ResponseListLead)
async def list_leads(
    service: LeadService = Depends(get_service_lead)
):
    return service.repo.get_list()

@router.post(
    "/",
    status_code=status.HTTP_201_CREATED,
    response_model=ResponseLead
)
async def create_operator(
    lead: CreateLead,
    service: LeadService = Depends(get_service_lead)
) -> Lead:
    return service.repo.create(lead)

# @router.put("/{id}", response_model=schemas.ResponseOperator)
# async def update_operator(
#     id: int,
#     operator: schemas.UpdateOperator,
#     service_operator: OperatorService = Depends(get_service_operator)
# ) -> Operator:
#     return service_operator.repo.update(id, operator)

@router.delete(
    "/{id}",
    status_code=status.HTTP_204_NO_CONTENT,
    responses={
        status.HTTP_404_NOT_FOUND: {
            "description": "Lead not found",
            "content": {
                "application/json": {
                    "example": {
                        "detail": "Lead with id 123 not found"
                    }
                },
            },
        },
        status.HTTP_204_NO_CONTENT: {"description": "Lead successfully deleted"},
    }
)
async def delete_operator(
    id: int,
    service: LeadService = Depends(get_service_lead)
) -> None:
        operator = service.repo.get(id)
        service.repo.delete(operator)

@router.get("/{id}/contacts", response_model=ResponseListContact)
async def get_contacts_by_lead(
    id: int,
    service: LeadService = Depends(get_service_lead)
):
    return service.get_contacts(id)
