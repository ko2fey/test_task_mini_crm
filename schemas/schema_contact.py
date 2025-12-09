from pydantic import BaseModel, ConfigDict
from datetime import datetime
from typing import Optional, List
from dependencies.custom_enum import StatusList


class BaseContact(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    operator_id: Optional[int] = None
    source_id: int
    lead_id: int
    
class CreateContact(BaseContact):
    status: StatusList =  StatusList.IN_QUEUE

class UpdateContact(BaseModel):
    status: StatusList
    operator_id: Optional[int] = None

class ResponseContact(BaseContact):
    id: int
    created_at: datetime
    updated_at: datetime
    status: StatusList

class ResponseListContact(BaseModel):
    objects: List[ResponseContact]
    total_count: int
    page: Optional[int] = None
    limit: Optional[int] = None
    order_by: Optional[str] = None
    order_type: Optional[str] = None

class FilterContact(BaseModel):
    source_id: Optional[int] = None
    operator_id: Optional[int] = None
    lead_id: Optional[int] = None
    status: Optional[StatusList] = None
    created_at_ge: Optional[datetime] = None
    created_at_le: Optional[datetime] = None
    updated_at_ge: Optional[datetime] = None
    updated_at_le: Optional[datetime] = None

