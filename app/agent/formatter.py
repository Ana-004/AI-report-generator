from datetime import date

from app import BaseAgent
from app import PipelineState


class FormatterAgent(BaseAgent):
    """Pure assembly, no LLM call - turns the reviewed draft into a final
    Markdown document. PDF/DOCX export will be added on top of this ;
    this agent's output is what the exporters will consume."""

    name = "formatter"

    def run(self, state: PipelineState) -> PipelineState:
        header = (
            f"# {state.topic}\n\n"
            f"*Generated {date.today().isoformat()} \u00b7 "
            f"Style: {state.style} \u00b7 Citation format: {state.citation_format}*\n\n"
            "---\n\n"
        )
        state.final_report = header + state.draft
        state.log("[formatter] assembled final report")
        return state
