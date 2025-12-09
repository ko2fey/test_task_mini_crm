from typing import Dict, Any, Optional, TYPE_CHECKING

if TYPE_CHECKING:
    from models import Operator

from repositories.repo_source import SourceRepository
from repositories.repo_operator import OperatorRepository
from repositories.repo_contact import DistributeRepository
from repositories.repo_lead import LeadRepository

from models import Contact

from services.service_base import BaseService

from dependencies.custom_enum import StatusList
from exceptions.exc_service import UnexpectedException
from exceptions.exc_base import RepositoryException
    


class DistributeService(BaseService[DistributeRepository, Contact]):
    def __init__(
        self, 
        source_repository: SourceRepository,
        operator_repository: OperatorRepository,
        lead_repository: LeadRepository,
        distribute_repository: DistributeRepository
    ):
        super().__init__(repo=distribute_repository)
        self.repo_source = source_repository
        self.repo_operator = operator_repository
        self.repo_lead = lead_repository 
    
    def update(self, id: int, data: Dict[str, Any]) -> Contact:
        if data.get('status', None):
            contact = self.repo.get(id)
            
            if data['status'] == StatusList.DONE:
                
                if contact.operator_id:
                    operator = self.repo_operator.get(contact.operator_id)
                    operator.decrement_current_loading()
                    self.repo.save()
            
                    
        return self.repo.update(id, data)
    
    def delete(self, object: Contact) -> None:
        try:
            if  object.operator_id:
                operator = self.repo_operator.get(object.operator_id)
                operator.decrement_current_loading()
                
            self.repo.delete(object)
            self.repo.save()
            
        except RepositoryException as e:
            self.repo.db.rollback()
            raise
        except Exception as e:
            self.repo.db.rollback()
            raise UnexpectedException(
                status_code=500,
                detail=f"Unexpected Error in Service Contact: {e}"
            ) from e
    
    def distribute_lead(self, data: Dict[str, Any]) -> Contact:
        try:
            # Find or create lead

            lead = self.repo_lead.find_by_external_id(data['external_id'])
            
            if lead is None:
                copy_data = data.copy()
                del copy_data['source_id']
                lead = self.repo_lead.create(copy_data)
            
            # Get source and add to lead. For model LeadsSources
            # SQLALchemy auto prevent add duplicate for relationship fields
            source = self.repo_source.get(data['source_id'])
            lead.sources.append(source)
            operator = self.select_best_operator(data['source_id'])
            
            contact_data: Dict[str, Any] = {
                "lead_id": lead.id,
                "source_id": data['source_id']
            }
            
            if operator:
                contact_data.update(
                    {
                        "operator_id": operator.id, 
                        "status": StatusList.NEW
                    }
                )

            # Create contact with operator or not  
            new_contact = self.repo.create(object=contact_data)
            if new_contact and operator:
                operator.increment_current_loading()
                self.repo_operator.save()
                
            return new_contact
        
        except Exception as e:
            self.repo.db.rollback()
            raise UnexpectedException(
                status_code=500,
                detail=f"Unexpected Error in Service Contact: {e}"
            ) from e
    
    def select_best_operator(self, source_id: int) -> Optional[Operator]:
        try:    
            available_operators = self.repo_operator.get_available_operator_for_source(source_id)
            
            if not available_operators:
                return None
                
            coefficients = []
            for operator in available_operators:
                weight = operator.get_priority_source(source_id)
                
                if weight is None:
                    continue
                
                coef = weight / max(operator.current_loading, 1)
                coefficients.append((operator, coef))
                            
            coefficients.sort(key=lambda x: (-x[1], x[0].current_loading))  
            
            print(f'Result: operator:{coefficients[0][0].id}, coef: {coefficients[0][1]}')
            return coefficients[0][0]
        except Exception as e:
            print(f"Error in service: contact, function: select_best_operator: {e}")
            return None
