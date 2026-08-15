from app.agent.base import BaseAgent
from app.state import PipelineState, Section

WRITER_SYSTEM_PROMPT = """You are the Writer Agent in a research report \
generation system. Write clear, well-structured prose for a single report \
section. Do not repeat the section title in the body text. Match the \
requested style. Do not fabricate citations, if you would normally cite a \
source, write [CITATION NEEDED] instead; the Citation Agent resolves these \
in a later phase once real sources are wired up."""


class WriterAgent(BaseAgent):
    name = "writer"

    def __init__(self, llm):
        self.llm = llm
        
    def run(self, state: PipelineState) -> PipelineState:
        for i, title in enumerate(state.outline):
            user_prompt = (
                f"Report topic: {state.topic}\n"
                f"Style: {state.style}\n"
                f"Section to write: {title}\n\n"
                "Write this section now."
            )
            content = self.llm.generate(WRITER_SYSTEM_PROMPT, user_prompt, max_tokens=800)
            state.sections[title] = Section(title=title, content=content, order=i)

        state.draft = "\n\n".join(
            f"## {s.title}\n\n{s.content}"
            for s in sorted(state.sections.values(), key=lambda s: s.order)
        )
        state.log(f"[writer] drafted {len(state.sections)} sections")
        return state
