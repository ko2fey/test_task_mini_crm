from .repo_base import BaseRepository
from models import OperatorSourcePriority
from sqlalchemy.orm import Session

class PriorityRepository(BaseRepository[OperatorSourcePriority]):
    
    def __init__(self, db:Session) -> None:
        super().__init__(model=OperatorSourcePriority, db=db)