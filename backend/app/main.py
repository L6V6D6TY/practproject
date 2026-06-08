from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import logging
import os
from app.config import config
from app.database import init_db
from app.routers import works
from app.scheduler import init_scheduler, shutdown_scheduler

# Настройка логирования
logging.basicConfig(
    level=getattr(logging, config.LOG_LEVEL),
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

# Создание приложения
app = FastAPI(
    title=config.APP_NAME,
    version=config.APP_VERSION,
    description="Приложение для обработки Excel файлов Наряд-допуски"
)

# CORS настройки
app.add_middleware(
    CORSMiddleware,
    allow_origins=config.CORS_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Подключение роутеров
app.include_router(works.router)

@app.on_event("startup")
async def startup_event():
    """Действия при запуске приложения"""
    logger.info("Запуск приложения...")
    
    # Инициализация БД
    init_db()
    logger.info("База данных инициализирована")
    
    # Запуск планировщика
    init_scheduler()
    
    logger.info("Приложение успешно запущено")

@app.on_event("shutdown")
async def shutdown_event():
    """Действия при остановке приложения"""
    logger.info("Остановка приложения...")
    shutdown_scheduler()
    logger.info("Приложение остановлено")

@app.get("/")
def root():
    """Корневой эндпоинт"""
    return {
        "message": f"{config.APP_NAME} API",
        "version": config.APP_VERSION,
        "status": "running"
    }

@app.get("/health")
def health_check():
    """Проверка здоровья приложения"""
    return {"status": "healthy"}

# ВРЕМЕННЫЙ ЭНДПОИНТ ДЛЯ РУЧНОЙ ЗАГРУЗКИ EXCEL
@app.post("/manual-load")
def manual_load():
    """Ручная загрузка Excel файла (временный эндпоинт для отладки)"""
    from app.services.excel_service import ExcelService
    from app.database import SessionLocal
    
    db = SessionLocal()
    try:
        service = ExcelService(db)
        success, message, count = service.load_and_process_excel()
        return {
            "success": success,
            "message": message,
            "count": count,
            "file_path": config.EXCEL_FULL_PATH,
            "folder": config.EXCEL_FOLDER_PATH,
            "filename": config.EXCEL_FILE_NAME
        }
    except Exception as e:
        return {
            "success": False,
            "message": str(e),
            "count": 0
        }
    finally:
        db.close()

        
@app.get("/test-db")
def test_db():
    from app.database import SessionLocal
    from app.models import SummaryWork
    
    db = SessionLocal()
    try:
        # Проверяем, есть ли данные
        count = db.query(SummaryWork).count()
        return {"success": True, "count": count, "message": f"В БД {count} записей"}
    except Exception as e:
        return {"success": False, "error": str(e)}
    finally:
        db.close()