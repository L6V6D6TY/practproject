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
    
    # Маппинг колонок Excel → поля БД
    COLUMN_MAPPING = {
        'Дата формирования наряда-допуска': 'doc_date',
        'Номер документа': 'doc_number',
        'Номер наряда-допуска': 'permit_number',
        'Статус': 'status',
        'Вид НД': 'work_type',
        'Организация': 'organization',
        'Подразделение': 'department',
        'Установка/Участок': 'unit',
        'Место проведения работ': 'work_location',
        'Содержание работ': 'work_content',
        'Дата начала план': 'plan_start_date',
        'Дата окончания план': 'plan_end_date',
        'Производитель работ': 'work_foreman',
        'Решение комиссии': 'commission_decision',
        'Комментарий': 'comment'
    }
    
    def __init__(self, db_session: Session):
        self.db_session = db_session
        self.staging_dao = StagingDAO(db_session)
        self.summary_dao = SummaryDAO(db_session)
    
    def load_excel_only(self) -> Tuple[bool, str, int]:
        """Только загрузка Excel в staging (без переноса в summary)"""
        file_path = config.EXCEL_FULL_PATH
        
        logger.info("=== НАЧАЛО load_excel_only ===")
        logger.info(f"Путь к файлу: {file_path}")
        
        try:
            if not os.path.exists(file_path):
                logger.error(f"Файл НЕ НАЙДЕН: {file_path}")
                raise FileNotFoundError(f"Файл не найден: {file_path}")
            
            logger.info(f"Файл найден, размер: {os.path.getsize(file_path)} байт")
            
            df = pd.read_excel(file_path, engine='openpyxl')
            logger.info(f"Прочитано строк: {len(df)}")
            logger.info(f"Колонки в Excel: {list(df.columns)}")
            
            df = df.rename(columns=self.COLUMN_MAPPING)
            logger.info(f"Колонки после маппинга: {list(df.columns)}")
            
            df = self._clean_data(df)
            logger.info(f"После очистки осталось строк: {len(df)}")
            
            if df.empty:
                logger.warning("Нет валидных данных после очистки")
                return False, "Нет валидных данных", 0
            
            staging_items = self._prepare_staging_data(df)
            logger.info(f"Подготовлено записей для staging: {len(staging_items)}")
            
            instances = []
            for item in staging_items:
                instance = self.staging_dao.create(**item)
                instances.append(instance)
            
            logger.info(f"Создано записей: {len(instances)}")
            self.db_session.commit()
            logger.info("=== КОНЕЦ load_excel_only (УСПЕШНО) ===")
            return True, f"Загружено {len(instances)} записей", len(instances)
            
        except Exception as e:
            logger.error(f"Ошибка: {str(e)}")
            self.db_session.rollback()
            logger.info("=== КОНЕЦ load_excel_only (ОШИБКА) ===")
            return False, str(e), 0
    
    def transfer_to_summary_and_clear(self) -> int:
        """Перенос всех данных из staging в summary и очистка staging"""
        logger.info("=== НАЧАЛО transfer_to_summary_and_clear ===")
        
        staging_items = self.staging_dao.get_all()
        logger.info(f"Найдено в staging: {len(staging_items)} записей")
        
        if not staging_items:
            logger.info("Нет данных в staging для переноса")
            return 0
        
        processed_count = 0
        for staging in staging_items:
            self.summary_dao.create_or_update(
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
                comment=staging.comment
            )
            processed_count += 1
            logger.debug(f"Обработано {processed_count} из {len(staging_items)}")
        
        # Очищаем staging
        self.staging_dao.clear()
        self.db_session.commit()
        
        logger.info(f"Перенесено {processed_count} записей, staging очищен")
        logger.info("=== КОНЕЦ transfer_to_summary_and_clear ===")
        return processed_count
    
    def _clean_data(self, df: pd.DataFrame) -> pd.DataFrame:
        """Очистка и приведение типов данных"""
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
        """Подготовка данных для промежуточной таблицы"""
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
                'file_name': config.EXCEL_FILE_NAME
            }
            items.append(item)
        return items