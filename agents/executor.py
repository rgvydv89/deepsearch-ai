class ExecutorAgent:
    def __init__(self, search_agent):
        self.search_agent = search_agent

    def execute_step(self, step):
        print(f"[Executor] Executing step: {step}")

        response = self.search_agent.run(step)

        # 🔥 Ensure correct format
        if not response or "results" not in response:
            return {"results": []}

        return {
            "results": response["results"]
        }