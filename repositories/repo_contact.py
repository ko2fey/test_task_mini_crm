from typing import Optional, TYPE_CHECKING

if TYPE_CHECKING:
    from dependencies.typed_dict import DictResponseList
    from schemas.schema_base import SortParams, PaginationParams
    from pydantic import BaseModel
            
from models import Contact
from sqlalchemy.orm import Session, Query
from sqlalchemy.exc import SQLAlchemyError

from repositories.repo_base import BaseRepository
from exceptions.exc_base import DatabaseException, UnexpectedException


class DistributeRepository(BaseRepository[Contact]):
    
    def __init__(self, db:Session) -> None:
        super().__init__(model=Contact, db=db)
    
    #Override methods _apply_filter, get_list from BaseRepository  
    def _apply_filter(
        self, 
        filter_params: BaseModel, 
        query: Query[Contact]
    ) -> Query[Contact]:
        cleaned_filter = filter_params \
            .model_dump(
                exclude_none=True, 
                exclude_unset=True
            )

        if cleaned_filter.get('operator_id', None):
            query = query.where(self.model.operator_id == cleaned_filter['operator_id'])
        
        if cleaned_filter.get('lead_id', None):
            query = query.where(self.model.lead_id == cleaned_filter['lead_id'])
            
        if cleaned_filter.get('source_id', None):
            query = query.where(self.model.source_id == cleaned_filter['source_id'])
            
        if cleaned_filter.get('created_at_ge', None):
            query = query.filter(self.model.created_at >= cleaned_filter['created_at_ge'])
        
        if cleaned_filter.get('created_at_le', None):
            query = query.filter(self.model.created_at <= cleaned_filter['created_at_le'])
        
        if cleaned_filter.get('updated_at_ge', None):
            query = query.filter(self.model.updated_at >= cleaned_filter['updated_at_ge'])
        
        if cleaned_filter.get('updated_at_le', None):
            query = query.filter(self.model.updated_at <= cleaned_filter['updated_at_le'])
        
        if cleaned_filter.get('status', None):
            query = query.filter(self.model.status == cleaned_filter['status'])  
        
        return query

    def get_list(self, 
        pagination: Optional[PaginationParams] = None,
        filter_params: Optional[BaseModel] = None,
        sort: Optional[SortParams] = None,
    ) -> DictResponseList[Contact]:
        try:
            query = self.db.query(self.model)
            response: DictResponseList[Contact] = {}
            
            if filter_params:
                query = self._apply_filter(
                    filter_params=filter_params, 
                    query=query, 
                )   
                
            if sort:    
                query = super()._apply_sort(sort=sort, query=query, response=response)   
            
            if pagination:    
                query = super()._apply_pagination(pagination=pagination, query=query, response=response)
            
            response.update(
                {
                    'objects': query.all(),
                    'total_count': query.count(),
                }
            )
                
            return response
        
        except SQLAlchemyError as e:
            raise DatabaseException(
                status_code=500, 
                detail=f"Database Error: {str(e)}"
            ) from e
            
        except Exception as e:
            raise UnexpectedException(
                status_code=500, 
                detail=f"Unexpected Error: {str(e)}"
            ) from e
     
    