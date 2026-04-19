import re

from orchestrator.message import Message


class ExecutorAgent:
    def __init__(self, mcp_client, decision_agent):
        self.mcp_client = mcp_client
        self.decision_agent = decision_agent

        self.metrics = {"steps": 0, "tool_calls": 0}

    # -----------------------------------------
    # 🔥 EXTRACT MATH EXPRESSION
    # -----------------------------------------
    def extract_expression(self, text):
        match = re.findall(r"[\d\.\+\-\*/\(\) ]+", text)
        return match[0].strip() if match else text

    # -----------------------------------------
    # MAIN HANDLE
    # -----------------------------------------
    async def handle(self, message):
        print(f"[Executor] Received message from {message.sender}")

        steps = message.content.get("steps", [])
        all_results = []

        tools = self.mcp_client.list_tools()

        for step in steps:
            if not isinstance(step, str):
                continue

            print(f"[Executor] Processing step: {step}")

            tool = self.decision_agent.decide_tool(step, tools)

            print(f"[Executor] Selected tool: {tool}")

            # ✅ count step
            self.metrics["steps"] += 1

            # =========================================
            # 🔥 SKIP NON-TOOL STEPS
            # =========================================
            if tool == "none":
                print("[Executor] Skipping non-tool step")
                continue

            # =========================================
            # 🔥 TOOL EXECUTION
            # =========================================
            try:
                if tool == "calculator":
                    expression = self.extract_expression(step)

                    print(f"[Executor] Clean expression: {expression}")

                    response = self.mcp_client.call("calculator", {"expression": expression})

                else:
                    response = self.mcp_client.call("search", {"query": step})

                # ✅ count only actual tool calls
                self.metrics["tool_calls"] += 1

            except Exception as e:
                print(f"[Executor ERROR]: {str(e)}")
                continue

            # =========================================
            # COLLECT RESULTS
            # =========================================
            if isinstance(response, dict) and "results" in response:
                all_results.extend(response["results"])

        return Message(
            sender="Executor",
            receiver="Reasoning",
            content={"results": all_results},
            msg_type="RESPONSE",
            status="SUCCESS",
            parent_id=message.id,
        )

    # -----------------------------------------
    # METRICS
    # -----------------------------------------
    def get_metrics(self):
        return self.metrics
