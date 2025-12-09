from typing import Optional
from dependencies.custom_enum import StatusList
from datetime import datetime

from sqlalchemy.orm import Session 
from fastapi import Depends, Query
from database import get_db
from schemas.schema_contact import FilterContact


from repositories.repo_priorities import PriorityRepository
from repositories.repo_operator import OperatorRepository
from repositories.repo_source import SourceRepository
from repositories.repo_lead import LeadRepository
from repositories.repo_contact import DistributeRepository

from services.service_operator import OperatorService
from services.service_priority import PriorityService
from services.service_source import SourceService
from services.service_lead import LeadService
from services.service_contact import DistributeService


def get_service_operator(db: Session = Depends(get_db)) -> OperatorService:
    repository = OperatorRepository(db)
    return OperatorService(repository)

def get_service_source(db: Session = Depends(get_db)) -> SourceService:
    repository = SourceRepository(db)
    return SourceService(repository)

def get_service_lead(db: Session = Depends(get_db)) -> LeadService:
    repository = LeadRepository(db)
    return LeadService(repository)

def get_service_priority(db: Session = Depends(get_db)) -> PriorityService:
    repo_op = OperatorRepository(db)
    repo_src = SourceRepository(db)
    repo_priority = PriorityRepository(db)
    
    return PriorityService(
        repo_priority=repo_priority,
        repo_operator=repo_op,
        repo_source=repo_src
    )

def get_service_distribute(db: Session = Depends(get_db)) -> DistributeService:
    repo_op = OperatorRepository(db)
    repo_src = SourceRepository(db)
    repo_lead = LeadRepository(db)
    repo_ditribute = DistributeRepository(db)
    
    return DistributeService(
        source_repository=repo_src,
        operator_repository=repo_op,
        lead_repository=repo_lead,
        distribute_repository=repo_ditribute
    )
    
def get_filter_params_contact(
    status: Optional[StatusList] = Query(None, description="Filter by status"),
    created_at_ge: Optional[datetime] = Query(None, description="Filter by date created from:", alias="created_from"),
    created_at_le: Optional[datetime] = Query(None, description="Filter by date created to:", alias="created_to"),
    updated_at_ge: Optional[datetime] = Query(None, description="Filter by date updated from:", alias="updated_from"),
    updated_at_le: Optional[datetime] = Query(None, description="Filter by date updated to:", alias="updated_to")
):
    
    return FilterContact(
        status=status,
        created_at_ge=created_at_ge,
        created_at_le=created_at_le,
        updated_at_ge=updated_at_ge,
        updated_at_le=updated_at_le
    )