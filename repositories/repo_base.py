from typing import TypeVar, Generic, Type, Optional, Callable, Dict, Any, TYPE_CHECKING

if TYPE_CHECKING:
    from schemas.schema_base import SortParams, PaginationParams
    from pydantic import BaseModel
    from sqlalchemy.orm import Session
    from sqlalchemy.orm.query import Query
    from dependencies.typed_dict import DictResponseList

from models import Base
        
from sqlalchemy.exc import SQLAlchemyError
from exceptions.exc_base import NotFoundException
from exceptions.exc_base import FailedUpdateException
from exceptions.exc_base import DatabaseException
from exceptions.exc_base import UnexpectedException



ModelType = TypeVar("ModelType", bound=Base)
RelatedType = TypeVar("RelatedType", bound=Base)

class BaseRepository(Generic[ModelType]):
    def __init__(self, model: Type[ModelType], db: Session):
        self.model = model
        self.db = db
    
    def _apply_sort(
        self, 
        sort: SortParams, 
        query: Query[RelatedType], 
        response: DictResponseList[RelatedType]
    ) -> Query[RelatedType]:
        if hasattr(self.model, sort.order_by):
            column = getattr(self.model, sort.order_by)
            query = query.order_by(
                column.asc() if sort.order_type == 'asc' else column.desc()
            )
            
            response.update(
                {
                    'order_type': sort.order_type,
                    'order_by': sort.order_by,   
                }
            )
            
        return query
    
    def _apply_pagination(
        self, 
        pagination: PaginationParams, 
        query: Query[RelatedType], 
        response: DictResponseList[RelatedType]
    ) -> Query[RelatedType]:
        query = query \
            .offset((pagination.page - 1) * pagination.limit) \
            .limit(pagination.limit)
            
        response.update(
            {
                'page': pagination.page,
                'limit': pagination.limit   
            }
        )
            
        return query
    
    def _apply_filter(
        self, 
        filter_params: BaseModel, 
        query: Query
    ) -> Query:
        cleaned_filter = filter_params \
            .model_dump(exclude_none=True, exclude_unset=True) \
            .items()
        for key, value in cleaned_filter:
            query = query.filter(getattr(self.model, key) == value)    
        
        return query

    def get_list(self, 
        pagination: Optional[PaginationParams] = None,
        filter_params: Optional[BaseModel] = None,
        sort: Optional[SortParams] = None,
    ) -> DictResponseList[ModelType]:
        try:
            query = self.db.query(self.model)
            response: DictResponseList[ModelType] = {}
            
            if filter_params:
                query = self._apply_filter(
                    filter_params=filter_params, 
                    query=query, 
                )
            
            total_count = query.count()    
                
            if sort:    
                query = self._apply_sort(sort=sort, query=query, response=response)   
            
            if pagination:    
                query = self._apply_pagination(pagination, query, response)
            
            response.update(
                {
                    'objects': query.all(),
                    'total_count': total_count,
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

    def create(self, object: Dict[str, Any]) -> ModelType:
        try:
            new_object = self.model(**object)     
            self.db.add(new_object)
            self.save()
            self.db.refresh(new_object)
            return new_object
        
        except SQLAlchemyError as e:
            self.db.rollback()
            raise DatabaseException(
                status_code=500, 
                detail=f"Database Error\n"
                       f"Failed to create object: {e}",
            ) from e
        
        except Exception as e:
            raise UnexpectedException(
                status_code=500, 
                detail=f"Unexpected Error\n"
                       f"Failed to create object: {e}"
            ) from e
        
    def update(
        self,
        id: int,
        data: Dict[str, Any],
    ) -> ModelType:
        try:
            object = self.get(id)   
                    
            for key, value in data.items():
                setattr(object, key, value)
            
            self.save()
            self.db.refresh(object)
            return object
        
        except SQLAlchemyError as e:
            self.db.rollback()
            raise DatabaseException(
                status_code=500, 
                detail=f"Database Error\n"
                       f"Failed to update object: {e}"
            ) from e
        
        except Exception as e:
            raise FailedUpdateException(
                detail=f"Failed to update object "
                       f"in Model {self.model.__name__} "
                       f"Error: {e} "
            ) from e
    
    def get(self, id: int) -> ModelType:
        object = self.db.query(self.model) \
            .filter(self.model.id == id).first() # type: ignore
        
        if object is None:
            raise NotFoundException(
                detail=f"Object with id={id} not found " 
                       f"in Model {self.model.__name__}"
                )
        
        return object
    
    def get_locked(self, id: int) -> ModelType:
        object = self.db.query(self.model) \
            .filter(self.model.id == id).with_for_update().first() # type: ignore
        
        if object is None:
            raise NotFoundException(
                detail=f"Object with id={id} not found " 
                       f"in Model {self.model.__name__}"
                )
        
        return object
    
    def delete(self, object: ModelType) -> None:
        try:        
            self.db.delete(object)
            self.save()
            
        except SQLAlchemyError as e:
            self.db.rollback()
            raise DatabaseException(
                status_code=500, 
                detail=f"Database Error\n"
                       f"Failed to delete object: {e}"
            ) from e
    
    def save(self) -> None:
        try:
            self.db.commit()
            
        except SQLAlchemyError as e:
            self.db.rollback()
            raise DatabaseException(
                status_code=500, 
                detail=f"Database Error\n"
                       f"Failed to save changes: {e}"
            ) from e
        
    def execute_with_locked(
        self, 
        id: int, 
        f: Callable[[ModelType], ModelType]
    ) -> ModelType:
        with self.db.begin():
            try:
                object = self.get_locked(id)
                result = f(object)
                self.save()
                return result
            
            except SQLAlchemyError as e:
                self.db.rollback()
                raise DatabaseException(
                    status_code=500, 
                    detail="Database Error\n"
                           "Failed to execute function\n" 
                           f"for changes in BEGIN LOCK BLOCK: {e}"
                ) from e
            except Exception as e:
                self.db.rollback()
                raise UnexpectedException(
                    status_code=500,
                    detail=f"Database Inexpected Error in BEGIN LOCK BLOCK: {e}"
                ) from e

