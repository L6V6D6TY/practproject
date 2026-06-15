import logging
from apscheduler.schedulers.background import BackgroundScheduler
from apscheduler.triggers.interval import IntervalTrigger
from apscheduler.triggers.cron import CronTrigger
from apscheduler.events import EVENT_JOB_EXECUTED, EVENT_JOB_ERROR
from app.config import config
from app.services.excel_service import ExcelService
from app.database import SessionLocal
import threading

logger = logging.getLogger(__name__)

scheduler = BackgroundScheduler()

# Блокировки для предотвращения одновременного выполнения
load_lock = threading.Lock()
aggregate_lock = threading.Lock()

def load_excel_to_staging():
    """Задача 1: загрузка Excel в промежуточную таблицу (каждые N минут)"""
    if not load_lock.acquire(blocking=False):
        logger.info("Загрузка Excel уже выполняется, пропускаем")
        return
    
    logger.info("=== ЗАПУСК load_excel_to_staging ===")
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
        load_lock.release()
        logger.info("=== КОНЕЦ load_excel_to_staging ===")

def aggregate_and_clear():
    """Задача 2: перенос из staging в summary и очистка staging (раз в день)"""
    if not aggregate_lock.acquire(blocking=False):
        logger.info("Агрегация уже выполняется, пропускаем")
        return
    
    logger.info("=== ЗАПУСК aggregate_and_clear ===")
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
        aggregate_lock.release()
        logger.info("=== КОНЕЦ aggregate_and_clear ===")

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