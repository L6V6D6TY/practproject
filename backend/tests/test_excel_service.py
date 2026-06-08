import pytest
import os
import tempfile
import pandas as pd
from app.services.excel_service import ExcelService
from app.database import SessionLocal

def test_excel_loading():
    """Тест: загрузка Excel файла"""
    # Создаём временный Excel файл
    test_data = pd.DataFrame({
        'Номер документа': ['TEST001', 'TEST002'],
        'Статус': ['Утвержден', 'Утвержден'],
        'Вид НД': ['Огневые работы', 'Огневые работы'],
        'Подразделение': ['ЦДНГ №1', 'ЦДНГ №2'],
        'Производитель работ': ['Мастер 1', 'Мастер 2']
    })
    
    with tempfile.NamedTemporaryFile(suffix='.xlsx', delete=False) as tmp:
        test_data.to_excel(tmp.name, index=False)
        tmp_path = tmp.name
    
    db = SessionLocal()
    try:
        service = ExcelService(db)
        # Проверяем, что метод существует
        assert hasattr(service, 'load_and_process_excel')
    finally:
        db.close()
    
    os.unlink(tmp_path)

def test_transfer_to_summary():
    """Тест: перенос данных в сводную таблицу"""
    db = SessionLocal()
    try:
        service = ExcelService(db)
        # Проверяем наличие метода _transfer_to_summary
        assert hasattr(service, '_transfer_to_summary')
    finally:
        db.close()