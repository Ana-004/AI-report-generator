#from app.llm.factory import LLMFactory
from app import (
    PlannerAgent,
    WriterAgent,
    ReviewerAgent,
    FormatterAgent,
)

shared_llm = LLMFactory().create()

planner = PlannerAgent(shared_llm)
writer = WriterAgent(shared_llm)
reviewer = ReviewerAgent(shared_llm)
formatter = FormatterAgent()


def planner_node(state):
    return planner.run(state)


def writer_node(state):
    return writer.run(state)


def reviewer_node(state):
    return reviewer.run(state)


def formatter_node(state):
    return formatter.run(state)