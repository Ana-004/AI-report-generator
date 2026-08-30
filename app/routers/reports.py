from fastapi import APIRouter, Depends, HTTPException
from fastapi.responses import Response

from sqlalchemy.orm import Session

from app import state
from app.database import get_db
from app.models import Report
from app.schemas import ReportRequest
from app.state import PipelineState

from app.graph.workflow import Orchestrator

from app.exporter.pdf_exporter import PDFExporter
from app.exporter.docx_exporter import DOCXExporter

router = APIRouter(prefix="/reports", tags=["reports"])


@router.post("/generate")
def generate_report(
    payload: ReportRequest,
    db: Session = Depends(get_db),
):

    # Create initial pipeline state
    state = PipelineState(
        topic=payload.topic,
        length=payload.length,
        style=payload.style,
        citation_format=payload.citation_format,
        model=payload.model
    )

     # Run multi-agent workflow
    try:
        state = Orchestrator(model=payload.model).run(state)

    except RuntimeError as exc:
        # e.g. ANTHROPIC_API_KEY missing
        raise HTTPException(
            status_code=500,
            detail=str(exc)
        ) from exc

    # Convert sections to JSON-compatible data
    sections_data = [
        {
            "title": section.title,
            "content": section.content,
            "order": section.order,
        }
        for section in state.sections.values()
    ]

    # Create database record
    report = Report(
        topic=state.topic,
        style=state.style,
        length=state.length,
        citation_format=state.citation_format,
        model=payload.model,
        content=state.final_report,
        sections=sections_data,
        agent_logs=state.agent_log,
    )

    # Save to PostgreSQL
    db.add(report)
    db.commit()
    db.refresh(report)

    # Return generated report
    return {
        "id": report.id,
        "topic": report.topic,
        "style": report.style,
        "length": report.length,
        "citation_format": report.citation_format,
        "content": report.content,
        "sections": report.sections,
        "agent_logs": report.agent_logs,
        "created_at": report.created_at,
    }

# GET RECENT REPORTS
@router.get("/recent")
def get_recent_reports(
    db: Session = Depends(get_db),
):
    reports = (
        db.query(Report)
        .order_by(
            Report.created_at.desc()
        )
        .limit(5)
        .all()
    )

    return [
        {
            "id": report.id,
            "topic": report.topic,
            "style": report.style,
            "length": report.length,
            "citation_format": report.citation_format,
            "created_at": report.created_at,
        }

        for report in reports
    ]

# GET LATEST REPORT
@router.get("/latest")
def get_latest_report(
    db: Session = Depends(get_db),
):
    report = (
        db.query(Report)
        .order_by(
            Report.created_at.desc()
        )
        .first()
    )

    if report is None:

        raise HTTPException(
            status_code=404,
            detail="No report has been generated.",
        )

    return {
        "id": report.id,
        "topic": report.topic,
        "style": report.style,
        "length": report.length,
        "citation_format": report.citation_format,
        "content": report.content,
        "sections": report.sections,
        "model": state.model,
        "agent_logs": report.agent_logs,
        "created_at": report.created_at,
    }

#GET SINGLE REPORT
@router.get("/{report_id}")
def get_report(
    report_id: int,
    db: Session = Depends(get_db),
):

    report = (
        db.query(Report)
        .filter(
            Report.id == report_id
        )
        .first()
    )

    if report is None:

        raise HTTPException(
            status_code=404,
            detail="Report not found.",
        )

    return {
        "id": report.id,
        "topic": report.topic,
        "style": report.style,
        "length": report.length,
        "citation_format": report.citation_format,
        "content": report.content,
        "sections": report.sections,
        "agent_logs": report.agent_logs,
        "created_at": report.created_at,
    }

# DOWNLOAD PDF
@router.get("/{report_id}/pdf")
def download_pdf(
    report_id: int,
    db: Session = Depends(get_db),
):

    report = (
        db.query(Report)
        .filter(
            Report.id == report_id
        )
        .first()
    )

    if report is None:

        raise HTTPException(
            status_code=404,
            detail="Report not found.",
        )

    # Generate PDF
    pdf_data = PDFExporter().export(
        report.content
    )

    # Clean filename
    filename = (
        report.topic
        .replace("/", "-")
        .replace("\\", "-")
        .replace(":", "-")
    )

    # Return PDF
    return Response(
        content=pdf_data,
        media_type="application/pdf",
        headers={
            "Content-Disposition":
                f'attachment; filename="{filename}.pdf"'
        },
    )

# DOWNLOAD DOCX
@router.get("/{report_id}/docx")
def download_docx(
    report_id: int,
    db: Session = Depends(get_db),
):

    report = (
        db.query(Report)
        .filter(
            Report.id == report_id
        )
        .first()
    )

    if report is None:

        raise HTTPException(
            status_code=404,
            detail="Report not found.",
        )

    # Generate DOCX
    docx_data = DOCXExporter().export(
        report.content
    )

    # Clean filename
    filename = (
        report.topic
        .replace("/", "-")
        .replace("\\", "-")
        .replace(":", "-")
    )

    # Return DOCX
    return Response(
        content=docx_data,
        media_type=(
            "application/vnd.openxmlformats-"
            "officedocument.wordprocessingml.document"
        ),
        headers={
            "Content-Disposition":
                f'attachment; filename="{filename}.docx"'
        },
    )