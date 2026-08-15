from fastapi import APIRouter, Depends, HTTPException

#from app import models
from app.graph.workflow import Orchestrator
from app.schemas import ReportRequest
from app.state import PipelineState
from app.reports import report_cache as cache

router = APIRouter(prefix="/reports", tags=["reports"])


@router.post("/generate")
def generate_report(payload: ReportRequest):
    state = PipelineState(
        topic=payload.topic,
        length=payload.length,
        style=payload.style,
        citation_format=payload.citation_format,
    )

    try:
        state = Orchestrator().run(state)
    except RuntimeError as exc:
        # e.g. ANTHROPIC_API_KEY missing
        raise HTTPException(status_code=500, detail=str(exc)) from exc

    # Save the report to cache
    cache.latest_report = {
        "topic": state.topic,
        "style": state.style,
        "length": state.length,
        "citation_format": state.citation_format,
        "content": state.final_report,
        "sections": [
            {
                "title": section.title,
                "content": section.content,
                "order": section.order,
            }
            for section in state.sections.values()
        ],
        "agent_logs": state.agent_log,
    }

    return cache.latest_report

@router.get("/latest")
def get_latest_report():
    if cache.latest_report is None:
        raise HTTPException(
            status_code =404,
            detail = "No report has been generated."
        )
    return cache.latest_report