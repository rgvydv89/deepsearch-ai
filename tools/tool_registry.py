import asyncio
from tools.calculator_tool import CalculatorTool
from tools.search_tool import SearchTool


class ToolRegistry:
    def __init__(self):
        self.tools = {
            "calculator": CalculatorTool(),
            "search": SearchTool()
        }

    def get_tool(self, tool_name):
        return self.tools.get(tool_name)

    async def execute(self, tool_name, query):
        tool = self.get_tool(tool_name)

        if not tool:
            print(f"[ToolRegistry] Tool not found: {tool_name}")
            return {"results": []}

        # 🔥 Handle async tool
        if asyncio.iscoroutinefunction(tool.run):
            return await tool.run(query)

        # 🔥 Handle sync tool
        return tool.run(query)