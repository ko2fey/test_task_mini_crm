from models import Contact
from sqlalchemy.orm import Session
from .repo_base import BaseRepository

class DistributeRepository(BaseRepository[Contact]):
    
    def __init__(self, db:Session) -> None:
        super().__init__(model=Contact, db=db)
    