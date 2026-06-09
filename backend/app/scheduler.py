import logging
from apscheduler.schedulers.background import BackgroundScheduler
from apscheduler.triggers.interval import IntervalTrigger
from apscheduler.triggers.cron import CronTrigger
from apscheduler.events import EVENT_JOB_EXECUTED, EVENT_JOB_ERROR
from app.config import config
from app.services.excel_service import ExcelService
from app.database import SessionLocal

logger = logging.getLogger(__name__)

scheduler = BackgroundScheduler()

def load_excel_to_staging():
    """Задача 1: загрузка Excel в промежуточную таблицу (каждые N минут)"""
    logger.info("Загрузка Excel в staging...")
    db = None
    try:
        db = SessionLocal()
        excel_service = ExcelService(db)
        success, message, count = excel_service.load_excel_only()
        if success:
            logger.info(f"Staging загружен: {message}")
        else:
            logger.error(f"Ошибка загрузки staging: {message}")
    except Exception as e:
        logger.error(f"Критическая ошибка: {str(e)}")
    finally:
        if db:
            db.close()

def aggregate_and_clear():
    """Задача 2: перенос из staging в summary и очистка staging (раз в день)"""
    logger.info("Агрегация данных и очистка staging...")
    db = None
    try:
        db = SessionLocal()
        excel_service = ExcelService(db)
        count = excel_service.transfer_to_summary_and_clear()
        logger.info(f"Агрегация завершена, обработано {count} записей")
    except Exception as e:
        logger.error(f"Ошибка агрегации: {str(e)}")
    finally:
        if db:
            db.close()

def init_scheduler() -> BackgroundScheduler:
    # Задача 1: загрузка из Excel в staging — каждые N минут
    scheduler.add_job(
        load_excel_to_staging,
        trigger=IntervalTrigger(minutes=config.SCHEDULE_INTERVAL_MINUTES),
        id="excel_ingest",
        replace_existing=True,
        max_instances=1
    )
    
    # Задача 2: агрегация и очистка — раз в день в 02:00
    scheduler.add_job(
        aggregate_and_clear,
        trigger=CronTrigger(hour=2, minute=0),
        id="aggregate_and_clear",
        replace_existing=True,
        max_instances=1
    )
    
    scheduler.start()
    logger.info(f"Планировщик запущен: ingest каждые {config.SCHEDULE_INTERVAL_MINUTES} мин, агрегация в 02:00")
    return scheduler

def shutdown_scheduler():
    if scheduler.running:
        scheduler.shutdown()
        logger.info("Планировщик остановлен")