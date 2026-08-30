from app.agent.researcher_base import ResearcherAgent
from app.state import Source

from app.services.tavily_client import TavilySearchClient

class WebResearcherAgent(ResearcherAgent):
    """Retrieves sources via simulated web search. In Phase 3, this would
    call a real search API (Google, DuckDuckGo, Bing) or use an LLM with
    web search (Claude via web search tool, etc.).
    
    For now, uses an LLM to simulate finding relevant URLs and extracting
    content — demonstrates the interface without external API setup."""

    name = "researcher_web"

    def __init__(
        self,
        tavily_client: TavilySearchClient,
        max_results: int = 5
        ):
            self.tavily_client = tavily_client
            self.max_results = max_results

    def retrieve(self,query: str) -> list[Source]:

        response = self.tavily_client.search(
            query=query,
            max_results=self.max_results,
        )

        sources = []

        for result in response.get(
            "results",
            []
        ):
            sources.append(
                Source(
                    title=result.get("title",""),
                    url=result.get("url",""),
                    raw_text=(result.get("raw_content")or result.get("content","")),
                    source_type="web",
                    provider="Tavily",
                )
            )

        return sources
