from pydantic import BaseModel
from typing import Optional, List
from datetime import datetime

class WorkBase(BaseModel):
    doc_number: str
    doc_date: Optional[datetime] = None
    status: Optional[str] = None
    work_type: Optional[str] = None
    department: Optional[str] = None
    unit: Optional[str] = None
    work_location: Optional[str] = None
    work_content: Optional[str] = None
    work_foreman: Optional[str] = None

class WorkCreate(WorkBase):
    pass

class WorkUpdate(BaseModel):
    status: Optional[str] = None
    work_type: Optional[str] = None
    department: Optional[str] = None
    work_foreman: Optional[str] = None

class WorkResponse(WorkBase):
    id: int
    load_count: int
    last_updated: datetime
    created_at: datetime
    
    class Config:
        from_attributes = True

class PaginatedResponse(BaseModel):
    items: List[WorkResponse]
    total: int
    page: int
    limit: int
    total_pages: int
    
    @classmethod
    def create(cls, items, total, page, limit):
        return cls(
            items=items,
            total=total,
            page=page,
            limit=limit,
            total_pages=(total + limit - 1) // limit
        )