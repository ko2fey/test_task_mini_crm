from exceptions.exc_base import NotFoundException
from models import Lead, Contact, Source
from sqlalchemy.orm import Session
from .repo_base import BaseRepository
from typing import Optional, List

class LeadRepository(BaseRepository[Lead]):
    
    def __init__(self, db: Session):
        super().__init__(model=Lead, db=db)
   
    def find_by_external_id(self, external_id: str) -> Optional[Lead]:
        lead =self.db.query(Lead).filter(Lead.external_id == external_id).first()
        return lead
    
    def get_list_contacts(self, id: int) -> List[Contact]:
        return self.get(id).contacts
    
    def get_list_sources(self, id: int) -> List[Source]:
        return self.get(id).sources