from schemas.schema_operator import ResponseOperator
from sqlalchemy.orm import Session
from sqlalchemy.exc import SQLAlchemyError
from models import Operator, OperatorSourcePriority
from repositories.repo_operator import OperatorRepository
from typing import List, Optional


class OperatorService:
    def __init__(self, repository: OperatorRepository) -> None:
        self.repo = repository
    
    def get_priorities(self, id: int):
        priorities = self.repo.get_list_priotiries(id)
        response = {
            'objects': priorities,
            'total_count': len(priorities)
        }
        return response
    
    def get_contacts(self, id: int):
        contacts = self.repo.get_list_contacts(id)
        response = {
            'objects': contacts,
            'total_count': len(contacts)
        }
        return response
    
    def increase_loading(self, id: int) -> ResponseOperator:       
        updated_operator = self.repo.execute_with_locked(id, self._increase)
        return ResponseOperator.model_validate(updated_operator)
    
    def decrease_loading(self, id: int) -> Operator:       
        operator = self.repo.execute_with_locked(id, self._decrease)
        return operator
        
    @staticmethod
    def _decrease(operator: Operator) -> Operator:
            if not operator.is_active:
                raise Exception(
                    f"Increase loading only for active operators"
                )
            
            operator.decrement_current_loading()
            return operator
    @staticmethod
    def _increase(operator: Operator) -> Operator:
        if not operator.is_active:
            raise Exception(
                f"Increase loading only for active operators"
            )
        
        operator.increment_current_loading()
        return operator
    