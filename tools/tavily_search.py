import os

from dotenv import load_dotenv
from tavily import TavilyClient

load_dotenv()


class TavilySearchTool:
    def __init__(self):
        api_key = os.getenv("TAVILY_API_KEY")

        if not api_key:
            raise ValueError("❌ TAVILY_API_KEY not found in .env")

        self.client = TavilyClient(api_key=api_key)

    def run(self, query):
        print(f"[TavilySearch] Searching: {query}")

        try:
            response = self.client.search(query=query, search_depth="advanced", max_results=3)

            results = []

            for r in response.get("results", []):
                results.append({"content": r.get("content", ""), "url": r.get("url", "")})

            return {"results": results}

        except Exception as e:
            print("[Tavily ERROR]:", e)
            return {"results": []}
