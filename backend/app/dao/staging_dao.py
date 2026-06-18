import logging
from typing import List, Optional, Dict, Any
from sqlalchemy.orm import Session
from app.dao.base_dao import BaseDAO
from app.models import StagingWork

logger = logging.getLogger(__name__)

class StagingDAO(BaseDAO[StagingWork]):
    
    def __init__(self, db_session: Session):
        super().__init__(StagingWork, db_session)
    
    def get_by_doc_number(self, doc_number: str) -> Optional[StagingWork]:
        return self.db.query(StagingWork).filter(
            StagingWork.doc_number == doc_number
        ).first()
    
    def batch_create(self, items: List[Dict[str, Any]]) -> List[StagingWork]:
        logger.info(f"batch_create: получено {len(items)} элементов")
        instances = []
        for i, item in enumerate(items):
            logger.debug(f"  Элемент {i}: doc_number={item.get('doc_number')}")
            instance = self.create(**item)
            instances.append(instance)
        self.db.flush()
        logger.info(f"batch_create: создано {len(instances)} записей")
        return instances
    
    def clear(self) -> int:
        count = self.db.query(StagingWork).count()
        logger.info(f"clear: удаляем {count} записей из staging")
        self.db.query(StagingWork).delete()
        return count