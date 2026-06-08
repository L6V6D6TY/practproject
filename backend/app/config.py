import os
from dotenv import load_dotenv

load_dotenv()

class Config:
    DATABASE_URL = os.getenv("DATABASE_URL", "postgresql://postgres:password@localhost:5432/excel_db")
    EXCEL_FOLDER_PATH = os.getenv("EXCEL_FOLDER_PATH", "C:/data/excel_files")
    EXCEL_FILE_NAME = os.getenv("EXCEL_FILE_NAME", "data.xlsx")
    SCHEDULE_INTERVAL_MINUTES = int(os.getenv("SCHEDULE_INTERVAL_MINUTES", "5"))
    CORS_ORIGINS = os.getenv("CORS_ORIGINS", "http://localhost:3000").split(",")
    LOG_LEVEL = os.getenv("LOG_LEVEL", "INFO")
    APP_NAME = "Excel Processor"
    APP_VERSION = "1.0.0"
    
    @property
    def EXCEL_FULL_PATH(self) -> str:
        """Полный путь к Excel файлу"""
        return os.path.join(self.EXCEL_FOLDER_PATH, self.EXCEL_FILE_NAME)

config = Config()