import requests


class BASEClient:

    BASE_URL = (
        "https://api.base-search.net/"
        "cgi-bin/BaseHttpSearchInterface.fcgi"
    )

    def search(
        self,
        query: str,
        limit: int = 5,
    ) -> list[dict]:

        params = {
            "func": "PerformSearch",
            "query": query,
            "hits": limit,
            "format": "json",
        }

        response = requests.get(
            self.BASE_URL,
            params=params,
            timeout=20,
        )

        response.raise_for_status()

        data = response.json()

        return data