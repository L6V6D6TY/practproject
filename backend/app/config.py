import os
from dotenv import load_dotenv

load_dotenv()

class Config:
    DATABASE_URL = os.getenv("DATABASE_URL", "postgresql://postgres:password@localhost:5432/excel_db")
    EXCEL_FOLDER_PATH = os.getenv("EXCEL_FOLDER_PATH", "C:/data/excel_files")
    EXCEL_FILE_NAME = os.getenv("EXCEL_FILE_NAME", "data.xlsx")
    SCHEDULE_INTERVAL_MINUTES = int(os.getenv("SCHEDULE_INTERVAL_MINUTES", "5"))

config = Config()
