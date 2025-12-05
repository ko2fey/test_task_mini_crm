from pydantic import BaseModel, ConfigDict
from datetime import datetime
from typing import Optional, List

class BaseLead(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    external_id: str

class CreateLead(BaseLead):
    pass

class UpdateLead(BaseModel):
    name: Optional[str] = None

class ResponseLead(BaseLead):
    id: int
    name: Optional[str]
    created_at: datetime

class ResponseListLead(BaseModel):
    objects: List[ResponseLead]
    page: Optional[int] = None
    limit: Optional[int] = None
    total_count: int

class AssignLead(BaseLead):
    source_id: int

class FilterLead(BaseModel):
    created_at: Optional[datetime]
