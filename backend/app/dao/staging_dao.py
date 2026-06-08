from typing import List, Optional, Dict, Any
from sqlalchemy.orm import Session
from sqlalchemy import and_
from app.dao.base_dao import BaseDAO
from app.models import StagingWork
import logging


logger = logging.getLogger(__name__)


class StagingDAO(BaseDAO[StagingWork]):
    
    def __init__(self, db_session: Session):
        super().__init__(StagingWork, db_session)
    
    def get_unprocessed(self) -> List[StagingWork]:
        """Получение необработанных записей"""
        return self.db.query(StagingWork).filter(StagingWork.processed == 0).all()
    
    def get_by_product_code(self, product_code: str) -> Optional[StagingWork]:
        """Получение записи по коду продукта"""
        return self.db.query(StagingWork).filter(
            StagingWork.product_code == product_code
        ).first()
    
    def get_by_doc_number(self, doc_number: str) -> Optional[StagingWork]:
        """Получение записи по номеру документа"""
        return self.db.query(StagingWork).filter(
            StagingWork.doc_number == doc_number
        ).first()
    
    def mark_as_processed(self, ids: List[int]) -> int:
        """Отметить записи как обработанные"""
        if not ids:
            return 0
        
        result = self.db.query(StagingWork).filter(
            StagingWork.id.in_(ids)
        ).update(
            {"processed": 1},
            synchronize_session=False
        )
        return result
    
    import logging
logger = logging.getLogger(__name__)

class StagingDAO(BaseDAO[StagingWork]):
    
    # ... остальные методы ...
    
    def batch_create(self, items: List[Dict[str, Any]]) -> List[StagingWork]:
        logger.info(f"=== batch_create: получено {len(items)} элементов ===")
        
        instances = []
        for i, item in enumerate(items):
            logger.info(f"Элемент {i}: doc_number={item.get('doc_number')}")
            
            # Проверяем, нет ли уже такого документа в staging
            existing = self.get_by_doc_number(item.get('doc_number'))
            if existing:
                logger.info(f"  -> Дубликат: {item.get('doc_number')} уже существует")
                continue
                
            logger.info(f"  -> Создаю новую запись")
            instance = self.create(**item)
            instances.append(instance)
            logger.info(f"  -> Создано, id={instance.id}")
        
        self.db.flush()
        logger.info(f"=== batch_create: создано {len(instances)} записей ===")
        return instances