from dotenv import load_dotenv

load_dotenv()

from fastapi import FastAPI  # (load_dotenv must run first)

from app import report 

app = FastAPI(
    title="AI Research Report Generator",
    version="0.1.0"
)

app.include_router(report.reports)


@app.on_event("startup")
def on_startup():
    init_db()


@app.get("/health")
def health():
    return {"status": "ok"}

@app.get("/latest")
def latest():
    return {"report": latest_report}