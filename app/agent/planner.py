#generate a structured outline for the report

from app import BaseAgent
#from app import call_llm
from app import PipelineState

PLANNER_SYSTEM_PROMPT = """You are the Planner Agent in a research report \
generation system. Given a topic, produce a clear section outline for a \
report of the requested length and style. Return ONLY a numbered list of \
section titles, one per line, nothing else - no preamble, no explanation."""

class PlannerAgent(BaseAgent):
    name = "planner"

    def run(self, state: PipelineState) -> PipelineState:
        user_prompt = (
            f"Topic: {state.topic}\n"
            f"Length: {state.length}\n"
            f"Style: {state.style}\n\n"
            "Produce the section outline."
        )
        raw = self.llm.generate(PLANNER_SYSTEM_PROMPT, user_prompt, max_tokens=300)

        outline = [
            line.split(".", 1)[-1].strip(" -")
            for line in raw.strip().splitlines()
            if line.strip()
        ]
        state.outline = outline or ["Introduction", "Body", "Conclusion"] # If LLM fails, the expression uses the fallback
        state.log(f"[planner] outline: {state.outline}")
        return state
