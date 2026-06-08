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
    """Сервис для обработки Excel файлов (Наряд-допуски)"""
    
    # Маппинг ваших Excel колонок → поля БД
    COLUMN_MAPPING = {
        'Дата формирования наряда-допуска': 'doc_date',
        'Номер документа': 'doc_number',
        'Номер наряда-допуска': 'permit_number',
        'Статус': 'status',
        'Вид НД': 'work_type',
        'Организация': 'organization',
        'Подразделение': 'department',
        'Установка/Частка': 'unit',
        'Место проведения работ': 'work_location',
        'Содержание работ': 'work_content',
        'Дата начала плана': 'plan_start_date',
        'Дата окончания плана': 'plan_end_date',
        'Производитель работ': 'work_foreman',
        'Решение комиссии': 'commission_decision',
        'Комментарий': 'comment'
    }
    
    def __init__(self, db_session: Session):
        self.db_session = db_session
        self.staging_dao = StagingDAO(db_session)
        self.summary_dao = SummaryDAO(db_session)
    
    def load_and_process_excel(self) -> Tuple[bool, str, int]:
        file_path = config.EXCEL_FULL_PATH
        
        try:
            if not os.path.exists(file_path):
                raise FileNotFoundError(f"Файл не найден: {file_path}")
            
            logger.info(f"=== НАЧАЛО ОБРАБОТКИ ===")
            logger.info(f"Файл: {file_path}")
            
            # Чтение Excel
            df = pd.read_excel(file_path, engine='openpyxl')
            logger.info(f"Прочитано строк: {len(df)}")
            logger.info(f"Колонки в Excel: {list(df.columns)}")
            
            # Переименование колонок
            df = df.rename(columns=self.COLUMN_MAPPING)
            logger.info(f"Колонки после маппинга: {list(df.columns)}")
            
            # Проверка наличия колонки doc_number
            if 'doc_number' not in df.columns:
                logger.error("Колонка 'doc_number' не найдена после маппинга!")
                return False, "Колонка 'Номер документа' не найдена", 0
            
            # Очистка данных
            df = self._clean_data(df)
            logger.info(f"После очистки осталось строк: {len(df)}")
            
            if df.empty:
                return False, "Нет валидных данных", 0
            
            # Сохранение в staging
            staging_items = self._prepare_staging_data(df)
            logger.info(f"Подготовлено записей для staging: {len(staging_items)}")
            
            created_items = self.staging_dao.batch_create(staging_items)
            self.db_session.commit()
            
            logger.info(f"Сохранено в staging: {len(created_items)}")
            
            # Перенос в summary
            processed_count = self._transfer_to_summary()
            
            logger.info(f"=== ОБРАБОТКА ЗАВЕРШЕНА: {processed_count} записей ===")
            
            return True, f"Обработано {processed_count} записей", processed_count
            
        except Exception as e:
            logger.error(f"Ошибка: {str(e)}", exc_info=True)
            return False, str(e), 0
    
    def _clean_data(self, df: pd.DataFrame) -> pd.DataFrame:
        df = df.copy()
        
        # Удаление строк без номера документа
        df = df.dropna(subset=['doc_number'])
        df = df[df['doc_number'].astype(str).str.strip() != '']
        df = df[df['doc_number'].astype(str).str.strip() != 'nan']
        
        # Обработка дат
        date_columns = ['doc_date', 'plan_start_date', 'plan_end_date']
        for col in date_columns:
            if col in df.columns:
                df[col] = pd.to_datetime(df[col], errors='coerce')
        
        # Обработка строк
        string_columns = ['doc_number', 'permit_number', 'status', 'work_type', 
                          'organization', 'department', 'unit', 'work_foreman', 
                          'commission_decision']
        for col in string_columns:
            if col in df.columns:
                df[col] = df[col].astype(str).str.strip()
                df[col] = df[col].replace('nan', '').replace('None', '')
        
        # Удаление дубликатов по номеру документа
        df = df.drop_duplicates(subset=['doc_number'], keep='first')
        
        return df
    
    def _prepare_staging_data(self, df: pd.DataFrame) -> List[Dict[str, Any]]:
        items = []
        for _, row in df.iterrows():
            item = {
                'doc_date': row.get('doc_date'),
                'doc_number': str(row.get('doc_number', '')),
                'permit_number': str(row.get('permit_number', '')),
                'status': str(row.get('status', '')),
                'work_type': str(row.get('work_type', '')),
                'organization': str(row.get('organization', '')),
                'department': str(row.get('department', '')),
                'unit': str(row.get('unit', '')),
                'work_location': str(row.get('work_location', '')),
                'work_content': str(row.get('work_content', '')),
                'plan_start_date': row.get('plan_start_date'),
                'plan_end_date': row.get('plan_end_date'),
                'work_foreman': str(row.get('work_foreman', '')),
                'commission_decision': str(row.get('commission_decision', '')),
                'comment': str(row.get('comment', '')),
                'file_name': config.EXCEL_FILE_NAME,
                'processed': 0
            }
            items.append(item)
        return items
    
    def _transfer_to_summary(self) -> int:
        unprocessed = self.staging_dao.get_unprocessed()
        if not unprocessed:
            return 0
        
        processed_ids = []
        for staging in unprocessed:
            existing = self.summary_dao.get_by_doc_number(staging.doc_number)
            
            if existing:
                existing.load_count += 1
                if staging.status:
                    existing.status = staging.status
                if staging.commission_decision:
                    existing.commission_decision = staging.commission_decision
            else:
                self.summary_dao.create(
                    doc_number=staging.doc_number,
                    permit_number=staging.permit_number,
                    doc_date=staging.doc_date,
                    status=staging.status,
                    work_type=staging.work_type,
                    organization=staging.organization,
                    department=staging.department,
                    unit=staging.unit,
                    work_location=staging.work_location,
                    work_content=staging.work_content,
                    plan_start_date=staging.plan_start_date,
                    plan_end_date=staging.plan_end_date,
                    work_foreman=staging.work_foreman,
                    commission_decision=staging.commission_decision,
                    comment=staging.comment,
                    load_count=1
                )
            
            processed_ids.append(staging.id)
        
        self.staging_dao.mark_as_processed(processed_ids)
        self.db_session.commit()
        
        return len(processed_ids)