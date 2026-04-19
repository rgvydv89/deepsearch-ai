class MCPClient:
    def __init__(self, server):
        self.server = server

    def list_tools(self):
        print("[MCP Client] Fetching available tools")
        return self.server.list_tools()

    def call(self, tool_name, arguments):
        print(f"[MCP Client] Calling tool: {tool_name}")
        return self.server.call_tool(tool_name, arguments)
