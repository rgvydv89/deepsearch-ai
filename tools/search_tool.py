class SearchTool:
    name = "search"
    description = "Search the web for relevant information based on a query"

    input_schema = {
        "type": "object",
        "properties": {
            "query": {"type": "string"}
        },
        "required": ["query"]
    }

    def execute(self, query):
        print(f"[SearchTool] Searching: {query}")

        return [
            {
                "title": f"Result for {query}",
                "url": f"https://example.com/{query.replace(' ', '_')}",  # ✅ FIX
                "content": f"Information about {query}"
            }
        ]