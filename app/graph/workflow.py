from langgraph.graph import StateGraph, START, END

from app.state import PipelineState

from app.agent.planner import PlannerAgent
from app.agent.writer import WriterAgent
from app.agent.reviewer import ReviewerAgent
from app.agent.formatter import FormatterAgent
from app.agent.webResearcher import WebResearcherAgent
from app.agent.acadResearcher import AcademicResearcherAgent

from app.graph.nodes import (
    planner_node,
    web_researcher_node,
    academic_researcher_node,
    writer_node,
    reviewer_node,
    formatter_node
)

from app.services.tavily_client import TavilySearchClient
from app.services.base_client import BASEClient

from app.llm.factory import LLMFactory


class Orchestrator:

    def __init__(self, model: str | None = None):

        self.model = model

        shared_llm = LLMFactory().create(model=self.model)

        # Research Services
        self.tavily_client = TavilySearchClient()
        self.base_client = BASEClient()

        # CREATE AGENTS
        self.planner = PlannerAgent(shared_llm)
        self.web_researcher = WebResearcherAgent(
            tavily_client=self.tavily_client,
            max_results=5
        )
        self.acad_researcher = AcademicResearcherAgent(
            base_client=self.base_client,
            results_per_source=5
        )
        self.writer = WriterAgent(shared_llm)
        self.reviewer = ReviewerAgent(shared_llm)
        self.formatter = FormatterAgent()

        #=========================================
        # LANGGRAPH
        #=========================================
        
        # Nodes
        builder = StateGraph(PipelineState)
        builder.add_node("planner", planner_node)
        builder.add_node("web_researcher",web_researcher_node)
        builder.add_node("academic_researcher",academic_researcher_node)
        builder.add_node("writer", writer_node)
        builder.add_node("reviewer", reviewer_node)
        builder.add_node("formatter", formatter_node)

        # Edges
        builder.add_edge(START, "planner")
        builder.add_edge("planner", "web_researcher")
        builder.add_edge("web_researcher", "academic_researcher")
        builder.add_edge("academic_researcher", "writer")
        builder.add_edge("writer", "reviewer")
        builder.add_edge("reviewer", "formatter")
        builder.add_edge("formatter", END)

        # COMPILE GRAPH
        self.graph = builder.compile()

    # RUN WORKFLOW
    def run(self, state: PipelineState):
        return self.graph.invoke(state)