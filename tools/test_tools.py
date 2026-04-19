from mcp.server import MCPServer


def main():
    server = MCPServer()

    print("\n--- Calculator Test ---")
    print(server.call("calculator", {"expression": "2+3*10"}))

    print("\n--- Search Test ---")
    print(server.call("search", {"query": "What is artificial intelligence?"}))


if __name__ == "__main__":
    main()
