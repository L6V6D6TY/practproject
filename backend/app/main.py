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

# ВРЕМЕННЫЕ ЭНДПОИНТЫ ДЛЯ ОТЛАДКИ (удалить после решения проблемы)
@app.post("/manual-load")
def manual_load():
    from app.services.excel_service import ExcelService
    from app.database import SessionLocal
    
    logger.info("=== РУЧНАЯ ЗАГРУЗКА EXCEL ===")
    db = SessionLocal()
    try:
        service = ExcelService(db)
        success, message, count = service.load_excel_only()
        logger.info(f"Результат: success={success}, count={count}, message={message}")
        return {"success": success, "message": message, "count": count}
    except Exception as e:
        logger.error(f"Ошибка: {str(e)}")
        return {"success": False, "error": str(e)}
    finally:
        db.close()

@app.get("/manual-load")
def manual_load():
    from app.services.excel_service import ExcelService
    from app.database import SessionLocal
    
    logger.info("=== РУЧНОЙ ПЕРЕНОС ИЗ STAGING В SUMMARY ===")
    db = SessionLocal()
    try:
        service = ExcelService(db)
        count = service.transfer_to_summary_and_clear()
        logger.info(f"Перенесено {count} записей")
        return {"success": True, "count": count}
    except Exception as e:
        logger.error(f"Ошибка: {str(e)}")
        return {"success": False, "error": str(e)}
    finally:
        db.close()