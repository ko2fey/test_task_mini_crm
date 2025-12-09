from schemas.schema_lead import AssignLead
from schemas.schema_contact import CreateContact

from repositories.repo_source  import SourceRepository
from repositories.repo_operator import OperatorRepository
from repositories.repo_contact import DistributeRepository
from repositories.repo_lead import LeadRepository

from dependencies.custom_enum import StatusList
from typing import List, Dict, Any
from time import time

class DestribureService:
    def __init__(
        self, 
        source_repository: SourceRepository,
        operator_repository: OperatorRepository,
        lead_repository: LeadRepository,
        contact_repository: DistributeRepository
        ):
        self.repo_source = source_repository
        self.repo_operator = operator_repository
        self.repo_lead = lead_repository
        self.repo_contact = contact_repository
    
    def distrebute_lead(self, data: AssignLead):
        # Find or create lead
        lead = self.repo_lead.find_by_external_id(data.external_id)
        
        if lead is None:
            lead = self.repo_lead.create(data)
        
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
        new_contact = self.repo_contact.create(CreateContact(**contact_data))
        return new_contact
    
    def select_best_operator(self, source_id: int):
        time_start = time()
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

        return coefficients[0][0]
        
    

            # best_operator, coef = max(
            #     coefficients, 
            #     key=lambda x: x[1]
            # )
        
        # return best_operator

            
            

from database import get_db
db = next(get_db())

repo_op = OperatorRepository(db)
repo_src = SourceRepository(db)
repo_lead = LeadRepository(db)
repo_contact = DistributeRepository(db)
service = DestribureService(
    lead_repository=repo_lead,
    operator_repository=repo_op,
    source_repository=repo_src,
    contact_repository=repo_contact
)

service.select_best_operator(2)

