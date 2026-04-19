class ResearchAgent:
    def __init__(self, executor):
        self.executor = executor

    def research(self, query):
        print("[ResearchAgent] Running multi-step research...")

        sub_queries = [
            f"{query} overview",
            f"{query} advantages",
            f"{query} disadvantages",
            f"{query} comparison",
        ]

        all_results = []

        for q in sub_queries:
            print(f"[ResearchAgent] Sub-query: {q}")

            result = self.executor.execute_step(q)

            if result and "results" in result:
                all_results.extend(result["results"])

        return all_results
