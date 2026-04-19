import os
import sys

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from tools.calculator import CalculatorTool
from tools.tavily_search import TavilySearchTool


class MCPServer:
    def __init__(self):
        self.tools = {"search": TavilySearchTool(), "calculator": CalculatorTool()}

    def call(self, tool_name, args):
        print(f"[MCP Server] Calling tool: {tool_name}")

        tool = self.tools.get(tool_name)

        if not tool:
            print("[MCP Server] Tool not found")
            return {"results": []}

        return tool.run(**args)

    # ✅ FIX
    def call_tool(self, tool_name, arguments):
        return self.call(tool_name, arguments)

    def list_tools(self):
        return [
            {"name": "search", "description": "Search the internet for information"},
            {"name": "calculator", "description": "Perform mathematical calculations"},
        ]
