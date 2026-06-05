from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import logging
from app.config import config
from app.database import init_db
from app.routers import works

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = FastAPI(title="Excel Processor", version="1.0.0")

app.add_middleware(
    CORSMiddleware,
    allow_origins=config.CORS_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(works.router)

@app.on_event("startup")
async def startup_event():
    logger.info("Запуск приложения...")
    init_db()
    logger.info("База данных инициализирована")

@app.get("/")
def root():
    return {"message": "Excel Processor API", "status": "running"}

@app.get("/health")
def health_check():
    return {"status": "healthy"}