from typing import TypedDict, List, TypeVar, Generic, Optional, TYPE_CHECKING

if TYPE_CHECKING:
    from dependencies.custom_enum import StatusList

ModelType = TypeVar('ModelType')
class DictResponseList(TypedDict, Generic[ModelType], total=False):
    objects: Optional[List[ModelType]]
    total_count: Optional[int]
    page: Optional[int]
    limit: Optional[int]
    order_by: Optional[str]
    order_type: Optional[str]
    
class DictBaseCreateModelObject(TypedDict, total=False):
    pass

class DictContact(DictBaseCreateModelObject, total=False):
    source_id: int
    lead_id: int
    operator_id: Optional[int]
    status: Optional[StatusList]

class DictLead(DictBaseCreateModelObject, total=False):
    name: Optional[str]
    external_id: str
    