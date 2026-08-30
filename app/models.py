# app/models.py

from datetime import datetime, timezone

from sqlalchemy import (
    Column,
    Integer,
    String,
    Text,
    DateTime,
)

from sqlalchemy.dialects.postgresql import JSONB

from app.database import Base


class Report(Base):

    __tablename__ = "reports"

    id = Column(
        Integer,
        primary_key=True,
        index=True,
    )

    # Report Information
    topic = Column(
        String(500),
        nullable=False,
    )

    style = Column(
        String(100),
        nullable=True,
    )

    length = Column(
        String(100),
        nullable=True,
    )

    citation_format = Column(
        String(100),
        nullable=True,
    )

    # Generated Report
    content = Column(
        Text,
        nullable=False,
    )

    # Structured Data
    sections = Column(
        JSONB,
        nullable=True,
    )

    agent_logs = Column(
        JSONB,
        nullable=True,
    )

    # Timestamp
    created_at = Column(
        DateTime(timezone=True),
        default=lambda: datetime.now(timezone.utc),
        nullable=False,
        index=True,
    )