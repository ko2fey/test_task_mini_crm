from models import Operator
from repositories.repo_operator import OperatorRepository

from services.service_base import BaseService


class OperatorService(BaseService[OperatorRepository, Operator]):
    def __init__(self, repository: OperatorRepository) -> None:
        super().__init__(repository)
   
    def get_priorities(self, id: int):
        priorities = self.repo.get_list_priotiries(id)
        response = {
            'objects': priorities,
            'total_count': len(priorities)
        }
        return response
    
    def atomic_increase_loading(self, id: int) -> Operator:       
        return self.repo.execute_with_locked(id, self._increase)
    
    def atomic_decrease_loading(self, id: int) -> Operator:       
        return self.repo.execute_with_locked(id, self._decrease)
    
    # Private static methods for use inside in execute_with_locked 
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
    