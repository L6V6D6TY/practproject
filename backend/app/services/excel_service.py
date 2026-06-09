def load_excel_only(self) -> Tuple[bool, str, int]:
    """Только загрузка Excel в staging (без переноса в summary)"""
    file_path = config.EXCEL_FULL_PATH
    
    try:
        if not os.path.exists(file_path):
            raise FileNotFoundError(f"Файл не найден: {file_path}")
        
        logger.info(f"Загрузка Excel в staging: {file_path}")
        df = pd.read_excel(file_path, engine='openpyxl')
        df = df.rename(columns=self.COLUMN_MAPPING)
        df = self._clean_data(df)
        
        if df.empty:
            return False, "Нет валидных данных", 0
        
        staging_items = self._prepare_staging_data(df)
        # batch_create без проверки дубликатов
        instances = []
        for item in staging_items:
            instance = self.staging_dao.create(**item)
            instances.append(instance)
        
        self.db_session.commit()
        return True, f"Загружено {len(instances)} записей", len(instances)
        
    except Exception as e:
        logger.error(f"Ошибка: {str(e)}")
        return False, str(e), 0

def transfer_to_summary_and_clear(self) -> int:
    """Перенос всех данных из staging в summary и очистка staging"""
    staging_items = self.staging_dao.get_all()
    
    if not staging_items:
        logger.info("Нет данных в staging для переноса")
        return 0
    
    processed_count = 0
    for staging in staging_items:
        # Используем существующий метод create_or_update
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
            comment=staging.comment,
            load_count=staging.load_count if hasattr(staging, 'load_count') else 1
        )
        processed_count += 1
    
    # Очищаем staging
    self.staging_dao.clear()
    self.db_session.commit()
    
    logger.info(f"Перенесено {processed_count} записей, staging очищен")
    return processed_count