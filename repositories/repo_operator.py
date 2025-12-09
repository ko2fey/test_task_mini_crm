from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from sqlalchemy.orm import Session
    
from sqlalchemy.orm import contains_eager
from models import Operator, OperatorSourcePriority
from repositories.repo_base import BaseRepository
from exceptions.exc_base import ForbiddenDeleteException, RepositoryException

class OperatorRepository(BaseRepository[Operator]):
    
    def __init__(self, db:Session) -> None:
        super().__init__(model=Operator, db=db)

    def get_list_priotiries(self, id: int):
        operator = self.get(id)
        return operator.priorities
    
    def get_list_contacts(self, id: int):
        operator = self.get(id)
        return operator.contacts

    def delete(self, object: Operator) -> None:
        try:
            if not object.can_delete():
                raise ForbiddenDeleteException(
                    detail=f"Operator with id={object.id} cannot be "
                           "deleted while has active loadings"
                )   
            super().delete(object)
            
        except RepositoryException as e:
            raise
 
    def get_available_operator_for_source(self, source_id: int) -> list[Operator]:
        return self.db.query(self.model) \
            .join(OperatorSourcePriority, self.model.priorities) \
            .filter(self.model.is_active) \
            .filter(self.model.is_available) \
            .filter(OperatorSourcePriority.source_id == source_id) \
            .options(contains_eager(self.model.priorities)) \
            .all()
    
    