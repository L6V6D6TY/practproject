import pytest
from app.dao.summary_dao import SummaryDAO
from app.dao.staging_dao import StagingDAO
from app.database import SessionLocal

def test_summary_dao_exists():
    """Тест: DAO существует"""
    db = SessionLocal()
    try:
        dao = SummaryDAO(db)
        assert dao is not None
    finally:
        db.close()

def test_staging_dao_exists():
    """Тест: DAO существует"""
    db = SessionLocal()
    try:
        dao = StagingDAO(db)
        assert dao is not None
    finally:
        db.close()

def test_mark_as_processed_empty():
    """Тест: отметка пустого списка"""
    db = SessionLocal()
    try:
        dao = StagingDAO(db)
        result = dao.mark_as_processed([])
        assert result == 0
    finally:
        db.close()