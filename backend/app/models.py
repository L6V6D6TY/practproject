from sqlalchemy import Column, Integer, String, DateTime, Text, Index
from sqlalchemy.sql import func
from app.database import Base

class StagingWork(Base):
    """Промежуточная таблица для сырых данных из Excel"""
    __tablename__ = "staging_works"
    
    id = Column(Integer, primary_key=True, index=True)
    doc_number = Column(String(50), nullable=False, index=True)
    doc_date = Column(DateTime, nullable=True)
    status = Column(String(50), nullable=True)
    work_type = Column(String(100), nullable=True)
    department = Column(String(100), nullable=True)
    unit = Column(String(200), nullable=True)
    work_location = Column(Text, nullable=True)
    work_content = Column(Text, nullable=True)
    work_foreman = Column(String(200), nullable=True)
    file_name = Column(String(255), nullable=True)
    loaded_at = Column(DateTime(timezone=True), server_default=func.now())
    processed = Column(Integer, default=0)
    permit_number = Column(String(50), nullable=True)
    organization = Column(String(200), nullable=True)
    plan_start_date = Column(DateTime, nullable=True)
    plan_end_date = Column(DateTime, nullable=True)
    commission_decision = Column(String(50), nullable=True)
    comment = Column(Text, nullable=True)

class SummaryWork(Base):
    """Сводная (накопительная) таблица"""
    __tablename__ = "summary_works"
    
    id = Column(Integer, primary_key=True, index=True)
    doc_number = Column(String(50), unique=True, nullable=False, index=True)
    doc_date = Column(DateTime, nullable=True)
    status = Column(String(50), nullable=True)
    work_type = Column(String(100), nullable=True)
    department = Column(String(100), nullable=True)
    unit = Column(String(200), nullable=True)
    work_location = Column(Text, nullable=True)
    work_content = Column(Text, nullable=True)
    work_foreman = Column(String(200), nullable=True)
    load_count = Column(Integer, default=1)
    last_updated = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now())
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    permit_number = Column(String(50), nullable=True)
    organization = Column(String(200), nullable=True)
    plan_start_date = Column(DateTime, nullable=True)
    plan_end_date = Column(DateTime, nullable=True)
    commission_decision = Column(String(50), nullable=True)
    comment = Column(Text, nullable=True)