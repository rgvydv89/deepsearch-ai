from orchestrator.message import Message


class ExecutorAgent:
    def __init__(self, mcp_client, decision_agent):
        self.mcp_client = mcp_client
        self.decision_agent = decision_agent

        self.metrics = {
            "steps": 0,
            "tool_calls": 0
        }

    async def handle(self, message):
        print(f"[Executor] Received message from {message.sender}")

        steps = message.content
        all_results = []

        tools = self.mcp_client.list_tools()

        for step in steps:
            if not isinstance(step, str):
                continue

            print(f"[Executor] Processing step: {step}")

            tool = self.decision_agent.decide_tool(step, tools)

            print(f"[Executor] Selected tool: {tool}")

            self.metrics["steps"] += 1
            self.metrics["tool_calls"] += 1

            if tool == "calculator":
                response = self.mcp_client.call(
                    "calculator",
                    {"expression": step}
                )
            else:
                response = self.mcp_client.call(
                    "search",
                    {"query": step}
                )

            if "results" in response:
                all_results.extend(response["results"])

        return Message(
            sender="Executor",
            receiver="Reasoning",
            content={"results": all_results}
        )

    def get_metrics(self):
        return self.metrics