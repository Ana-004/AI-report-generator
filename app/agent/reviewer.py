from app import BaseAgent
from app import PipelineState

REVIEWER_SYSTEM_PROMPT = """You are the Reviewer Agent. Read the full draft \
report and rewrite it to fix clarity, flow, and consistency issues across \
sections, while preserving all factual content and every [CITATION NEEDED] \
marker exactly as-is. Return the complete corrected report in Markdown, \
section headers included — nothing else."""


class ReviewerAgent(BaseAgent):
    name = "reviewer"

    def run(self, state: PipelineState) -> PipelineState:
        user_prompt = f"Draft report:\n\n{state.draft}"
        reviewed = self.llm.generate(REVIEWER_SYSTEM_PROMPT, user_prompt, max_tokens=3000)
        state.draft = reviewed
        state.review_notes = "Reviewed for clarity, flow, and consistency."
        state.log("[reviewer] pass complete")
        return state
