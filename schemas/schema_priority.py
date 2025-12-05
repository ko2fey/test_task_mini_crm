from pydantic import BaseModel, ConfigDict
from typing import Optional, List
from datetime import datetime

class BasePriority(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    operator_id: int
    source_id: int
    weight: int
    
class CreatePriority(BasePriority):
    pass

class UpdatePriority(BaseModel):
    weight: int

class ResponsePriority(BasePriority):
    id: int
    created_at: datetime
    updated_at: datetime
    
class ResponseListPriority(BaseModel):
    objects: List[ResponsePriority]
    total_count: int
    