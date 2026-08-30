from app import state
from app.llm.factory import LLMFactory
from app.services.tavily_client import TavilySearchClient 
from app.services.base_client import BASEClient

from app.agent.planner import PlannerAgent
from app.agent.writer import WriterAgent
from app.agent.reviewer import ReviewerAgent
from app.agent.formatter import FormatterAgent
from app.agent.webResearcher import WebResearcherAgent
from app.agent.acadResearcher import AcademicResearcherAgent

# SHARED LLM
shared_llm = LLMFactory().create()
# RESEARCH SERVICES
tavily_client = TavilySearchClient() 
base_client = BASEClient()

# AGENTS
planner = PlannerAgent(shared_llm)
writer = WriterAgent(shared_llm)
reviewer = ReviewerAgent(shared_llm)
formatter = FormatterAgent()
web_researcher = WebResearcherAgent(
    tavily_client=tavily_client,
    max_results=5
)
acad_researcher = AcademicResearcherAgent(
    base_client=base_client,
    results_per_source=5
)


# LANGGRAPH NODES
def planner_node(state):
    """ Planner creates the report outline. """
    planner = PlannerAgent(
        model=state.model
    )
    return planner.run(state)

def web_researcher_node(state): 
    """ Tavily searches the web and adds web sources to state.sources. """ 
    web_researcher = WebResearcherAgent(
        tavily_client=tavily_client,
        max_results=5
    )
    return web_researcher.run(state)

def academic_researcher_node(state): 
    """ BASE searches academic literature and adds academic sources to state.sources. """ 
    acad_researcher = AcademicResearcherAgent(
        base_client=base_client,
        results_per_source=5
    )
    return acad_researcher.run(state)

def writer_node(state):
    """ Writer creates the initial draft of the report. """
    writer = WriterAgent(
        model=state.model
    )
    return writer.run(state)


def reviewer_node(state):
    """ Reviewer evaluates the draft and provides feedback. """
    reviewer = ReviewerAgent(
        model=state.model
    )
    return reviewer.run(state)


def formatter_node(state):
    """ Formatter formats the final report. """
    return formatter.run(state)