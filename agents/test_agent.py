import re

# ======================
# TOOLS
# ======================


class CalculatorTool:
    def run(self, query):
        try:
            expression = re.findall(r"[\d\.\+\-\*/\(\)]+", query)
            expression = "".join(expression)
            return eval(expression)
        except:
            return "Calculation error"


class SearchTool:
    def run(self, query):
        return f"[Search result for]: {query}"


# ======================
# TOOL REGISTRY
# ======================

tool_registry = {"calculator": CalculatorTool(), "search": SearchTool()}


# ======================
# EXECUTOR
# ======================


class ExecutorAgent:
    def __init__(self, tool_registry):
        self.tool_registry = tool_registry

    def execute_step(self, query, tool):
        print(f"[Executor] Tool: {tool}")

        if tool in self.tool_registry:
            return self.tool_registry[tool].run(query)

        return "No tool matched"


# ======================
# DECISION (NO LLM FOR NOW)
# ======================


class DecisionAgent:
    def decide_tool(self, query):

        if re.search(r"\d+\s*[\+\-\*/]\s*\d+", query):
            return "calculator"

        return "search"


# ======================
# MAIN
# ======================

if __name__ == "__main__":
    decision_agent = DecisionAgent()
    executor = ExecutorAgent(tool_registry)

    query = input("Enter query: ")

    context = query

    for step in range(2):  # simple loop
        print(f"\n[Agent Step {step+1}]")

        tool = decision_agent.decide_tool(context)

        result = executor.execute_step(context, tool)

        # 🔥 OBSERVE (important)
        context = f"{context}\nObservation: {result}"

    print("\nFinal Answer:", result)
