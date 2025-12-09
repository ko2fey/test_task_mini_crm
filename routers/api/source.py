from fastapi import APIRouter, Depends, status

from schemas.schema_source import CreateSource, UpdateSource, ResponseSource
from schemas.schema_source import ResponseListSource
from schemas.schema_contact import ResponseListContact, FilterContact

from models import Source

from services.service_source import SourceService
from services.service_contact import DistributeService

from dependencies.dependencies import get_service_source
from dependencies.dependencies import get_service_distribute
from dependencies.dependencies import get_filter_params_contact

router = APIRouter(
    prefix="/sources",
    tags=["sources"],
)

@router.get("/", response_model=ResponseListSource)
async def list_sources(
    service: SourceService = Depends(get_service_source)
):
    return service.repo.get_list()

@router.post(
    "/", 
    response_model=ResponseSource)
async def create_source(
    source: CreateSource,
    service: SourceService = Depends(get_service_source)
) -> Source:
    return service.repo.create(
        source.model_dump(exclude_unset=True, exclude_none=True)
    )

@router.put("/{id}", response_model=ResponseSource)
async def update_source(
    id: int,
    source: UpdateSource,
    service: SourceService = Depends(get_service_source)
) -> Source:
    return service.repo.update(
        id, 
        source.model_dump(exclude_unset=True, exclude_none=True)
    )

@router.delete(
    "/{id}",
    status_code=status.HTTP_204_NO_CONTENT,
    responses={
        status.HTTP_404_NOT_FOUND: {
            "description": "Source not found",
            "content": {
                "application/json": {
                    "example": {
                        "detail": "Source with id 123 not found"
                    }
                },
            },
        },
        status.HTTP_204_NO_CONTENT: {"description": "Source successfully deleted"},
    }
)
async def delete_source(
    id: int,
    service: SourceService = Depends(get_service_source)
) -> None:
        source = service.repo.get(id)
        service.repo.delete(source)

@router.get("/{id}/contacts", response_model=ResponseListContact)
async def get_contacts_by_source(
    id: int,
    service: DistributeService = Depends(get_service_distribute),
    filter_params: FilterContact = Depends(get_filter_params_contact),    
):
    extended_filter_params = filter_params.model_copy(update={"source_id": id})
    return service.repo.get_list(filter_params=extended_filter_params)
