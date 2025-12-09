from pydantic import BaseModel, ConfigDict
from typing import Optional, List

class BaseOperator(BaseModel):
    name: str
    max_loading: int = 10
    current_loading: int = 0
    active: bool = True
    
class CreateOperator(BaseModel):
    name: str
    max_loading: int = 10
    active: bool = True

class UpdateOperator(BaseModel):
    name: Optional[str] = None
    active: Optional[bool] = None
    max_loading: Optional[int] = None
    current_loading: Optional[int] = None

class ResponseOperator(BaseOperator):
    model_config = ConfigDict(from_attributes=True)
    id: int
    
class ResponseListOperator(BaseModel):
    objects: List[ResponseOperator]
    total_count: int
    page: Optional[int] = None
    limit: Optional[int] = None
    order_by: Optional[str] = None
    order_type: Optional[str] = None

class FilterOperator(BaseModel):
    active: Optional[bool] = None