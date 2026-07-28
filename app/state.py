"""
Shared pipeline state passed between agents during report generation.

Every agent reads from and writes to this. It is one object
that lets the Orchestrator chain agents together without
knowing anything about how any individual agent works internally.
"""

from dataclasses import dataclass, field

#With @dataclass (@ -> decorator) python automatically creates the constructor (__init__)
@dataclass
class Section:
    title: str
    content: str = ""
    order: int = 0


@dataclass
class Source:
    """Populated starting Phase 3 by the Researcher Agent."""
    url: str = ""
    title: str = ""
    raw_text: str = ""


@dataclass
class PipelineState:
    # --- input ---
    topic: str
    length: str = "medium"          # short | medium | long
    style: str = "academic"         # academic | business | technical
    citation_format: str = "APA"    # APA | MLA | Chicago | IEEE

    # --- planner output ---
    outline: list[str] = field(default_factory=list)

    # --- researcher output (Phase 3) ---
    sources: list[Source] = field(default_factory=list)

    # --- writer output ---
    sections: dict[str, Section] = field(default_factory=dict)
    draft: str = ""

    # --- reviewer output ---
    review_notes: str = ""

    # --- formatter output ---
    final_report: str = ""

    # --- observability ---
    agent_log: list[str] = field(default_factory=list)

    def log(self, message: str) -> None:
        self.agent_log.append(message)