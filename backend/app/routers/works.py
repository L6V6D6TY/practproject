from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from typing import Optional
from app.database import get_db
from app.services.work_service import WorkService
from app.schemas import WorkCreate, WorkUpdate, WorkResponse, PaginatedResponse

router = APIRouter(prefix="/api/works", tags=["works"])

@router.get("/", response_model=PaginatedResponse)
def get_works(
    db: Session = Depends(get_db),
    page: int = Query(1, ge=1),
    limit: int = Query(100, ge=1, le=100),
    field: Optional[str] = Query(None),
    value: Optional[str] = Query(None)
):
    service = WorkService(db)
    works, total = service.get_all_works_paginated(
        page=page, limit=limit, field=field, value=value
    )
    return PaginatedResponse.create(
        items=works, total=total, page=page, limit=limit
    )

@router.get("/{work_id}", response_model=WorkResponse)
def get_work(work_id: int, db: Session = Depends(get_db)):
    service = WorkService(db)
    work = service.get_work_by_id(work_id)
    if not work:
        raise HTTPException(status_code=404, detail="Запись не найдена")
    return work

@router.post("/", response_model=WorkResponse, status_code=201)
def create_work(work: WorkCreate, db: Session = Depends(get_db)):
    service = WorkService(db)
    try:
        new_work = service.create_work(work)
        db.commit()  # ← коммит только здесь
        return new_work
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.put("/{work_id}", response_model=WorkResponse)
def update_work(work_id: int, work_update: WorkUpdate, db: Session = Depends(get_db)):
    service = WorkService(db)
    updated_work = service.update_work(work_id, work_update)
    if not updated_work:
        raise HTTPException(status_code=404, detail="Запись не найдена")
    db.commit()  # ← коммит только здесь
    return updated_work

@router.delete("/{work_id}", status_code=204)
def delete_work(work_id: int, db: Session = Depends(get_db)):
    service = WorkService(db)
    if not service.delete_work(work_id):
        raise HTTPException(status_code=404, detail="Запись не найдена")
    db.commit()  # ← коммит только здесь
    return None