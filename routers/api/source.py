from fastapi import APIRouter, Depends, status
from schemas.schema_source import CreateSource, UpdateSource, ResponseSource
from schemas.schema_source import ResponseListSource
from schemas.schema_contact import ResponseListContact

from models import Source

from services.service_source import SourceService

from dependencies import get_service_source

router = APIRouter(
    prefix="/sources",
    tags=["sources"],
)

# Создать ИСТОЧНИК
@router.get("/", response_model=ResponseListSource)
async def list_sources(
    service: SourceService = Depends(get_service_source)
):
    return service.repo.get_list()

@router.post(
    "/", 
    response_model=ResponseSource)
async def create_operator(
    source: CreateSource,
    service: SourceService = Depends(get_service_source)
) -> Source:
    return service.repo.create(source)

@router.put("/{id}", response_model=ResponseSource)
async def update_operator(
    id: int,
    source: UpdateSource,
    service: SourceService = Depends(get_service_source)
) -> Source:
    return service.repo.update(id, source)

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
async def delete_operator(
    id: int,
    service: SourceService = Depends(get_service_source)
) -> None:
        source = service.repo.get(id)
        service.repo.delete(source)

@router.get("/{id}/contacts", response_model=ResponseListContact)
async def get_contacts_by_source(
    id: int,
    service: SourceService = Depends(get_service_source)    
):
    return service.get_contacts(id)
