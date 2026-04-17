from tools.search_tool import SearchTool
from tools.calculator_tool import CalculatorTool


class MCPServer:
    def __init__(self):
        self.tools = {
            "search": SearchTool(),
            "calculator": CalculatorTool()
        }

    def list_tools(self):
        return [
            {
                "name": tool.name,
                "description": tool.description,
                "input_schema": tool.input_schema
            }
            for tool in self.tools.values()
        ]

    def call_tool(self, tool_name, arguments):
        print(f"[MCP Server] Calling tool: {tool_name}")

        if tool_name not in self.tools:
            return {"results": [], "error": "Tool not found"}

        tool = self.tools[tool_name]

        try:
            result = tool.execute(**arguments)
            return {"results": result}
        except Exception as e:
            return {"results": [], "error": str(e)}