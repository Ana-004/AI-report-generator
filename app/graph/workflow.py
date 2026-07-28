from langgraph.graph import StateGraph, START, END

from app import PipelineState
from app import (
    PlannerAgent,
    WriterAgent,
    ReviewerAgent,
    FormatterAgent,
)

from app import (
    planner_node,
    writer_node,
    reviewer_node,
    formatter_node
)

from app import LLMFactory


class Orchestrator:

    def __init__(self):

        shared_llm = LLMFactory().create()

        self.planner = PlannerAgent(shared_llm)
        self.writer = WriterAgent(shared_llm)
        self.reviewer = ReviewerAgent(shared_llm)
        self.formatter = FormatterAgent()

        builder = StateGraph(PipelineState)
        builder.add_node("planner", planner_node)
        builder.add_node("writer", writer_node)
        builder.add_node("reviewer", reviewer_node)
        builder.add_node("formatter", formatter_node)

        builder.add_edge(START, "planner")
        builder.add_edge("planner", "writer")
        builder.add_edge("writer", "reviewer")
        builder.add_edge("reviewer", "formatter")
        builder.add_edge("formatter", END)

        self.graph = builder.compile()

    def run(self, state: PipelineState):
        return self.graph.invoke(state)