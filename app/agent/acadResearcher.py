from app.agent.researcher_base import ResearcherAgent
from app.state import Source

from app.services.base_client import BASEClient


class AcademicResearcherAgent(ResearcherAgent):

    name = "researcher_academic"

    def __init__(
        self,
        base_client: BASEClient,
        results_per_source: int = 5,
    ):

        self.base_client = base_client
        self.results_per_source = results_per_source

    def retrieve(self,query: str) -> list[Source]:

        try:
            response = self.base_client.search(
                query=query,
                limit=self.results_per_source,
            )

            return self._parse_results(response)

        except Exception as e:

            print(
                f"BASE search failed: {e}"
            )

            return []

    def _parse_results(
        self,
        data: dict
    ) -> list[Source]:

        sources = []

        results = (
            data
            .get("response", {})
            .get("docs", [])
        )

        for item in results:

            authors = item.get("author",[])

            if isinstance(
                authors,
                str
            ):
                authors = [authors]

            sources.append(
                Source(
                    title=item.get("title","Untitled"),
                    url=(item.get("url")or item.get("link") or ""),
                    raw_text=item.get("abstract",""),
                    authors=authors,
                    year=str(item.get("year","")),
                    source_type="academic",
                    provider="BASE",
                    external_id=str(item.get("id",""))
                )
            )

        return sources