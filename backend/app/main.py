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