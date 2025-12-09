from typing import Optional, TYPE_CHECKING

if TYPE_CHECKING:
    from sqlalchemy.orm import Session

    
from models import Source
from .repo_base import BaseRepository
from exceptions.exc_base import RepositoryException, ForbiddenDeleteException

class SourceRepository(BaseRepository[Source]):
    
    def __init__(self, db:Session) -> None:
        super().__init__(model=Source, db=db)
    
    def delete(self, object: Source) -> None:
        try:
            if not object.can_delete():
                raise ForbiddenDeleteException(
                    detail=f"Cannot be deleted while has active contacts with this source"
                )   
            super().delete(object)
            
        except RepositoryException as e:
            raise