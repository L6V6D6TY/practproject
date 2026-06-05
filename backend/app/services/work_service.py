from typing import List, Optional, Tuple
from sqlalchemy.orm import Session
from app.dao.summary_dao import SummaryDAO
from app.schemas import WorkCreate, WorkUpdate

class WorkService:
    def __init__(self, db: Session):
        self.db = db
        self.dao = SummaryDAO(db)
    
    def get_all(
        self, page: int = 1, limit: int = 100, field: str = None, value: str = None
    ) -> Tuple[List, int]:
        return self.dao.filter_with_pagination(page, limit, field, value)
    
    def get_by_id(self, work_id: int):
        return self.dao.get_by_id(work_id)
    
    def create(self, data: WorkCreate):
        existing = self.dao.get_by_doc_number(data.doc_number)
        if existing:
            raise ValueError(f"Документ {data.doc_number} уже существует")
        return self.dao.create(**data.model_dump())
    
    def update(self, work_id: int, data: WorkUpdate):
        work = self.dao.get_by_id(work_id)
        if not work:
            return None
        update_data = {k: v for k, v in data.model_dump().items() if v is not None}
        return self.dao.update(work, **update_data)
    
    def delete(self, work_id: int) -> bool:
        work = self.dao.get_by_id(work_id)
        if work:
            self.dao.delete(work)
            self.db.commit()
            return True
        return False