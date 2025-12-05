from schemas.schema_priority import CreatePriority
from repositories.repo_priorities import PriorityRepository
from repositories.repo_operator import OperatorRepository
from repositories.repo_source import SourceRepository
from models import OperatorSourcePriority
from exceptions.exc_base import RepositoryException
from exceptions.exc_service import UnexpectedException

class PriorityService:
    def __init__(
        self, 
        repo_priority: PriorityRepository, 
        repo_operator: OperatorRepository,
        repo_source: SourceRepository
    ) -> None:
        self.repo_priority = repo_priority
        self.repo_operator = repo_operator
        self.repo_source = repo_source
    
    def assign_priority(
        self, 
        data: CreatePriority
    ) -> OperatorSourcePriority:
        try:
            operator = self.repo_operator.get(data.operator_id)
            source = self.repo_source.get(data.source_id)
            new_priority = self.repo_priority.create(data)
            return new_priority
        
        except RepositoryException as e:
            raise
        
        except Exception as e:
            raise UnexpectedException(
                status_code=500,
                detail=f"Unexpected Error in Service Priorities: {e}"
            ) from e
            
        