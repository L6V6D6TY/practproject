from typing import List, Dict, Any
from sqlalchemy.orm import Session
from app.dao.base_dao import BaseDAO
from app.models import StagingWork

class StagingDAO(BaseDAO[StagingWork]):
    def __init__(self, db: Session):
        super().__init__(StagingWork, db)
    
    def get_unprocessed(self) -> List[StagingWork]:
        return self.db.query(StagingWork).filter(StagingWork.processed == 0).all()
    
    def get_by_doc_number(self, doc_number: str):
        return self.db.query(StagingWork).filter(StagingWork.doc_number == doc_number).first()
    
    def mark_as_processed(self, ids: List[int]) -> int:
        if not ids:
            return 0
        return self.db.query(StagingWork).filter(StagingWork.id.in_(ids)).update(
            {"processed": 1}, synchronize_session=False
        )
    
    def batch_create(self, items: List[Dict[str, Any]]) -> List[StagingWork]:
        instances = []
        for item in items:
            existing = self.get_by_doc_number(item.get('doc_number'))
            if not existing:
                instance = self.create(**item)
                instances.append(instance)
        return instances