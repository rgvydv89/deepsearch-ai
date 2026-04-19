import os

from dotenv import load_dotenv
from tavily import TavilyClient

from tools.utils import clean_search_query


class SearchAgent:
    def __init__(self):
        load_dotenv()
        self.client = TavilyClient(api_key=os.getenv("TAVILY_API_KEY"))

    def run(self, query: str):
        clean_query = clean_search_query(query)

        print("[DEBUG] Searching for:", clean_query)

        try:
            response = self.client.search(query=clean_query, search_depth="basic")

            results = response.get("results", [])

            print("[DEBUG] Raw Tavily response:", response)

            return {"query": clean_query, "results": results}

        except Exception as e:
            print("[ERROR] Tavily failed:", str(e))
            return {"query": clean_query, "results": []}
