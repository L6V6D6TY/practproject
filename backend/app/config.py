import os
from dotenv import load_dotenv

load_dotenv()

class Config:
    # Database
    DATABASE_URL = os.getenv("DATABASE_URL", "postgresql://postgres:password@localhost:5432/excel_db")
    
    # Excel
    EXCEL_FOLDER_PATH = os.getenv("EXCEL_FOLDER_PATH", "C:/data/excel_files")
    EXCEL_FILE_NAME = os.getenv("EXCEL_FILE_NAME", "data.xlsx")
    
    @property
    def EXCEL_FULL_PATH(self):
        return os.path.join(self.EXCEL_FOLDER_PATH, self.EXCEL_FILE_NAME)
    
    # Scheduler
    SCHEDULE_INTERVAL_MINUTES = int(os.getenv("SCHEDULE_INTERVAL_MINUTES", "5"))
    
    # API
    CORS_ORIGINS = os.getenv("CORS_ORIGINS", "http://localhost:3000").split(",")

config = Config()