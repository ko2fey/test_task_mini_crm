from pydantic import BaseModel, ConfigDict
from enum import Enum
from datetime import datetime
from typing import Optional, List
from custom_enum import StatusList


class BaseContact(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    operator_id: Optional[int] = None
    source_id: int
    lead_id: int
    
class CreateContact(BaseContact):
    status: StatusList =  StatusList.IN_QUEUE

class UpdateContact(BaseModel):
    status: StatusList

class ResponseContact(BaseContact):
    id: int
    created_at: datetime
    updated_at: datetime
    status: StatusList

class ResponseListContact(BaseModel):
    objects: List[ResponseContact]
    total_count: int
    order_by: Optional[str] = None
    order_type: Optional[str] = None

