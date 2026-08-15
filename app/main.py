from dotenv import load_dotenv

from app.reports import report_cache

load_dotenv()

from fastapi import FastAPI  # (load_dotenv must run first)

from app.reports import report 
from app.reports import report_cache as cache

app = FastAPI(
    title="AI Research Report Generator",
    version="0.1.0"
)

app.include_router(report.router)

@app.get("/health")
def health():
    return {"status": "ok"}

@app.get("/latest")
def latest():
    return {"report": cache.latest_report}