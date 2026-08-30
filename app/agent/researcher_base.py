from abc import abstractmethod

from app.agent.base import BaseAgent
from app.state import PipelineState, Source


class ResearcherAgent(BaseAgent):
    """Base class for researcher variants. Each implements retrieve() to
    fetch content from its specific source (web, PDF, database, etc.).
    All write to state.sources, so multiple researchers can run and their
    findings merge automatically."""

    name = "researcher"

    @abstractmethod
    def retrieve(self, query: str) -> list[Source]:
        """Return a list of Source objects for this query. The agent is
        responsible for fetching title, url, raw_text as much as possible."""
        ...

    def run(self, state: PipelineState) -> PipelineState:
        """Retrieve sources for the report topic and add them to state."""
        sources = self.retrieve(state.topic)
        state.sources.extend(sources)
        state.log(f"[{self.name}] retrieved {len(sources)} sources")
        return state
