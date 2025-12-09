from typing import Optional, List, TYPE_CHECKING

if TYPE_CHECKING:
    from models import Source
    from sqlalchemy.orm import Session
    
from models import Lead
from .repo_base import BaseRepository

class LeadRepository(BaseRepository[Lead]):
    
    def __init__(self, db: Session):
        super().__init__(model=Lead, db=db)
   
    def find_by_external_id(self, external_id: str) -> Optional[Lead]:
        return self.db.query(self.model) \
            .where(self.model.external_id == external_id) \
            .first()
           
    def get_list_sources(self, id: int) -> List[Source]:
        return self.get(id).sources