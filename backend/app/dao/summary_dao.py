from typing import List, Optional, Tuple
from sqlalchemy.orm import Session
from sqlalchemy import String, Integer
from app.dao.base_dao import BaseDAO
from app.models import SummaryWork

class SummaryDAO(BaseDAO[SummaryWork]):
    def __init__(self, db: Session):
        super().__init__(SummaryWork, db)
    
    def get_by_doc_number(self, doc_number: str) -> Optional[SummaryWork]:
        return self.db.query(SummaryWork).filter(SummaryWork.doc_number == doc_number).first()
    
    def filter_with_pagination(
        self, page: int = 1, limit: int = 100, field: str = None, value: str = None
    ) -> Tuple[List[SummaryWork], int]:
        query = self.db.query(SummaryWork)
        
        if field and value:
            column = getattr(SummaryWork, field, None)
            if column:
                if isinstance(column.type, String):
                    query = query.filter(column.ilike(f"%{value}%"))
                elif isinstance(column.type, Integer):
                    try:
                        query = query.filter(column == int(value))
                    except ValueError:
                        pass
        
        total = query.count()
        offset = (page - 1) * limit
        items = query.offset(offset).limit(limit).all()
        return items, total
    
    def create_or_update(self, **kwargs) -> SummaryWork:
        doc_number = kwargs.get('doc_number')
        existing = self.get_by_doc_number(doc_number)
        
        if existing:
            existing.load_count += 1
            self.db.flush()
            return existing
        else:
            return self.create(**kwargs)