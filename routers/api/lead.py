from schemas.schema_lead import CreateLead, UpdateLead
from schemas.schema_lead import ResponseLead, ResponseListLead
from schemas.schema_contact import ResponseListContact, FilterContact
from schemas.schema_source import ResponseListSource

from models import Lead

from services.service_lead import LeadService

from dependencies.dependencies import get_service_lead
from dependencies.dependencies import get_service_distribute
from dependencies.dependencies import get_filter_params_contact

from fastapi import APIRouter, Depends, status


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
async def create_lead(
    lead: CreateLead,
    service: LeadService = Depends(get_service_lead)
) -> Lead:
    return service.repo.create(lead.model_dump(exclude_unset=True, exclude_none=True))

@router.put("/{id}", response_model=ResponseLead)
async def update_lead(
    id: int,
    data: UpdateLead,
    service: LeadService = Depends(get_service_lead)
) -> Lead:
    return service.repo.update(
        id, 
        data.model_dump(exclude_unset=True, exclude_none=True)
    )

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
async def delete_lead(
    id: int,
    service: LeadService = Depends(get_service_lead)
) -> None:
        lead = service.repo.get(id)
        service.repo.delete(lead)

@router.get("/{id}/contacts", response_model=ResponseListContact)
async def get_contacts_by_lead(
    id: int,
    service: LeadService = Depends(get_service_distribute),
    filter_params: FilterContact = Depends(get_filter_params_contact),
):
    extended_filter_params = filter_params.model_copy(update={"lead_id": id})
    return service.repo.get_list(filter_params=extended_filter_params)

@router.get("/{id}/sources", response_model=ResponseListSource)
async def get_sources_by_lead(
    id: int,
    service: LeadService = Depends(get_service_lead)
):
    return service.get_sources(id)
