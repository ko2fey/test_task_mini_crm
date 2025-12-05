from pydantic import BaseModel, ConfigDict
from datetime import datetime
from typing import Optional, List

class BaseSource(BaseModel):
    name: str

class CreateSource(BaseSource):
    pass

class UpdateSource(BaseModel):
    name: Optional[str] = None

class ResponseSource(BaseSource):
    model_config = ConfigDict(from_attributes=True)
    id: int

class ResponseListSource(BaseModel):
    objects: List[ResponseSource]
    page: Optional[int] = None
    limit: Optional[int] = None
    total_count: int

class FilterSource(BaseModel):
    created_at: Optional[datetime]