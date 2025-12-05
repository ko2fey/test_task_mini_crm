from pydantic import BaseModel

class PaginationParams(BaseModel):
    page: int
    limit: int

class SortParams(BaseModel):
    order_by: str = 'id'
    order_type: str = 'asc'