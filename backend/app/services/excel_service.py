import pandas as pd
import os
import logging
from typing import Tuple, List, Dict, Any
from sqlalchemy.orm import Session
from app.dao.staging_dao import StagingDAO
from app.dao.summary_dao import SummaryDAO
from app.config import config

logger = logging.getLogger(__name__)

class ExcelService:
    COLUMN_MAPPING = {
        'Дата формирования наряда-допуска': 'doc_date',
        'Номер документа': 'doc_number',
        'Статус': 'status',
        'Вид НД': 'work_type',
        'Подразделение': 'department',
        'Установка/Участок': 'unit',
        'Место проведения работ': 'work_location',
        'Содержание работ': 'work_content',
        'Производитель работ': 'work_foreman',
    }
    
    def __init__(self, db: Session):
        self.db = db
        self.staging_dao = StagingDAO(db)
        self.summary_dao = SummaryDAO(db)
    
    def load_and_process_excel(self) -> Tuple[bool, str, int]:
        file_path = config.EXCEL_FULL_PATH
        
        if not os.path.exists(file_path):
            return False, f"Файл не найден: {file_path}", 0
        
        try:
            df = pd.read_excel(file_path, sheet_name='Наряд-допуски', engine='openpyxl')
            df = df.rename(columns=self.COLUMN_MAPPING)
            
            # Очистка
            df = df.dropna(subset=['doc_number'])
            df['doc_number'] = df['doc_number'].astype(str).str.strip()
            
            # Сохранение в staging
            items = []
            for _, row in df.iterrows():
                items.append({
                    'doc_number': str(row.get('doc_number', '')),
                    'doc_date': row.get('doc_date'),
                    'status': str(row.get('status', '')),
                    'work_type': str(row.get('work_type', '')),
                    'department': str(row.get('department', '')),
                    'unit': str(row.get('unit', '')),
                    'work_location': str(row.get('work_location', '')),
                    'work_content': str(row.get('work_content', '')),
                    'work_foreman': str(row.get('work_foreman', '')),
                    'file_name': config.EXCEL_FILE_NAME,
                    'processed': 0
                })
            
            created = self.staging_dao.batch_create(items)
            self.db.commit()
            
            # Перенос в summary
            count = self._transfer_to_summary()
            
            return True, f"Обработано {count} записей", count
        except Exception as e:
            logger.error(f"Ошибка: {str(e)}")
            return False, str(e), 0
    
    def _transfer_to_summary(self) -> int:
        unprocessed = self.staging_dao.get_unprocessed()
        count = 0
        
        for staging in unprocessed:
            self.summary_dao.create_or_update(
                doc_number=staging.doc_number,
                doc_date=staging.doc_date,
                status=staging.status,
                work_type=staging.work_type,
                department=staging.department,
                unit=staging.unit,
                work_location=staging.work_location,
                work_content=staging.work_content,
                work_foreman=staging.work_foreman,
            )
            count += 1
        
        self.staging_dao.mark_as_processed([s.id for s in unprocessed])
        self.db.commit()
        return count