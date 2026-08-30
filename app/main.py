from dotenv import load_dotenv

load_dotenv()

from app.database import Base, engine
from fastapi import FastAPI  # (load_dotenv must run first)

from app.routers.reports import router as reports_router
from app.routers import report_cache as cache

# CREATE DATABASE TABLES
Base.metadata.create_all(
    bind=engine
)

# FASTAPI APPLICATION
app = FastAPI(
    title="AI Research Report Generator",
    description="Multi-Agent AI Research Report Generator",
    version="1.0.0"
)

# ROUTERS
app.include_router(reports_router)

# ROOT
@app.get("/")
def root():

    return {
        "message": "ResearchForge API is running."
    }

@app.get("/health")
def health():
    return {"status": "ok"}

@app.get("/latest")
def latest():
    return {"report": cache.latest_report}