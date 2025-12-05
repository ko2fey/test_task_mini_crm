from fastapi import Depends
from database import get_db
from sqlalchemy.orm import Session

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