from sqlalchemy import Column, Integer, String, DateTime
from sqlalchemy.sql import func
from app.database import Base

class StagingWork(Base):
    __tablename__ = "staging_works"
    id = Column(Integer, primary_key=True, index=True)
    doc_number = Column(String(50), nullable=False, index=True)
    status = Column(String(50), nullable=True)
    loaded_at = Column(DateTime(timezone=True), server_default=func.now())
    processed = Column(Integer, default=0)

class SummaryWork(Base):
    __tablename__ = "summary_works"
    id = Column(Integer, primary_key=True, index=True)
    doc_number = Column(String(50), unique=True, nullable=False, index=True)
    status = Column(String(50), nullable=True)
    last_updated = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now())

    