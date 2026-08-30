"""
Shared pipeline state passed between agents during report generation.

Every agent reads from and writes to this. It is one object
that lets the Orchestrator chain agents together without
knowing anything about how any individual agent works internally.
"""

from dataclasses import dataclass, field

#With @dataclass (@ -> decorator ) python automatically creates the constructor (__init__)
@dataclass
class Section:
    title: str
    content: str = ""
    order: int = 0


@dataclass
class Source:
    title: str = ""
    url: str = ""
    raw_text: str = ""

    # Research metadata
    authors: list[str] = field(default_factory=list)
    year: str = ""
    doi: str = ""

    # Where the source came from
    source_type: str = ""       # academic / web
    provider: str = ""          # BASE / Tavily
    external_id: str = ""


@dataclass
class PipelineState:
    # --- input ---
    topic: str
    length: str = "medium"          # short | medium | long
    style: str = "academic"         # academic | business | technical
    citation_format: str = "APA"    # APA | MLA | Chicago | IEEE
    model: str = "gpt-4"                 # gpt-4 | gpt-3.5-turbo | custom

    # --- planner output ---
    outline: list[str] = field(default_factory=list)      #creates a new list every time

    # --- researcher output ---
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