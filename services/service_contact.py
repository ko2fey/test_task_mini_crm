from schemas.schema_lead import AssignLead, CreateLead
from schemas.schema_contact import CreateContact
from repositories.repo_source  import SourceRepository
from repositories.repo_operator import OperatorRepository
from repositories.repo_contact import DistributeRepository
from repositories.repo_lead import LeadRepository

from models import Contact, Operator
from custom_enum import StatusList
from typing import List, Dict, Any, Optional


class DistributeService:
    def __init__(
        self, 
        source_repository: SourceRepository,
        operator_repository: OperatorRepository,
        lead_repository: LeadRepository,
        distribute_repository: DistributeRepository
        ):
        self.repo_source = source_repository
        self.repo_operator = operator_repository
        self.repo_lead = lead_repository
        self.repo_distribute = distribute_repository
    
    def distrebute_lead(self, data: AssignLead) -> Contact:
        # Find or create lead
        lead = self.repo_lead.find_by_external_id(data.external_id)
        
        if lead is None:
            lead = self.repo_lead.create(
                CreateLead(
                    **data.model_dump(
                        exclude_none=True, 
                        exclude_unset=True, 
                        exclude={"source_id"}
                    )
                )
            )
        
        # Get source and add to lead. For model LeadsSources
        source = self.repo_source.get(data.source_id)
        lead.sources.append(source)
        # Select best availeble operator
        operator = self.select_best_operator(data.source_id)
        
        contact_data: Dict[str, Any] = {
            "lead_id": lead.id,
            "source_id": data.source_id
        }
        
        if operator:
            contact_data.update(
                {
                    "operator_id": operator.id, 
                    "status": StatusList.NEW
                }
            )

        # Create contact with operator or not  
        new_contact = self.repo_distribute.create(CreateContact(**contact_data))
        if new_contact and operator:
            operator.increment_current_loading()
            self.repo_operator.save()
        return new_contact
    
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
                
                # print(f'Operator: {operator.id}, weight: {weight}, coef: {coef}')              
            coefficients.sort(key=lambda x: (-x[1], x[0].current_loading))  
            
            print(f'Result: operator:{coefficients[0][0].id}, coef: {coefficients[0][1]}')
            return coefficients[0][0]
        except Exception as e:
            print(f"Error in service: contact, function: select_best_operator: {e}")
            return None
