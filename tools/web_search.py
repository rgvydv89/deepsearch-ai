from tavily import TavilyClient
import os

class WebSearchTool:
    def __init__(self):
        self.client = TavilyClient(api_key="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")

    def search(self, query: str, max_results: int = 5):
        response = self.client.search(
            query=query,
            max_results=max_results
        )
        
        results = []
        for r in response['results']:
            results.append({
                "title": r["title"],
                "url": r["url"],
                "content": r["content"]
            })
        
        return results