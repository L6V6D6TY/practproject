import logging
from apscheduler.schedulers.background import BackgroundScheduler
from apscheduler.triggers.interval import IntervalTrigger
from app.config import config
from app.services.excel_service import ExcelService
from app.database import SessionLocal

logger = logging.getLogger(__name__)
scheduler = BackgroundScheduler()

def scheduled_excel_loading():
    logger.info("Запуск загрузки Excel")
    db = SessionLocal()
    try:
        service = ExcelService(db)
        success, message, count = service.load_and_process_excel()
        if success:
            logger.info(f"Успех: {message}")
        else:
            logger.error(f"Ошибка: {message}")
    finally:
        db.close()

def init_scheduler():
    scheduler.add_job(
        scheduled_excel_loading,
        trigger=IntervalTrigger(minutes=config.SCHEDULE_INTERVAL_MINUTES),
        id="excel_loading",
        replace_existing=True,
    )
    scheduler.start()
    logger.info(f"Планировщик запущен (интервал: {config.SCHEDULE_INTERVAL_MINUTES} мин)")

def shutdown_scheduler():
    if scheduler.running:
        scheduler.shutdown()