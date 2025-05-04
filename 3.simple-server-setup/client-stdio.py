import asyncio
import nest_asyncio
from mcp import ClientSession, StdioServerParameters
from mcp.client.stdio import stdio_client

"""
Make sure:
1. The server is configured to use stdio transport.
"""

nest_asyncio.apply() # This is required for the stdio transport and run interactive python code

async def main():
    # This helps to run the server.py file so the MCP Server
    server_parameters = StdioServerParameters(
        command="python",
        args=["server.py"],
    )
    # Connect to the server
    async with stdio_client(server_parameters) as (read_stream, write_stream):
        async with ClientSession(read_stream, write_stream) as session:
            await session.initialize()

            tool_result = await session.list_tools()
            print("Available tools:")
            for tool in tool_result.tools:
                print(f" - {tool.name}: {tool.description}")

            # Call our calculator tool
            result = await session.call_tool("add", arguments={"a": 1, "b": 2})
            print(f"Result of add(1, 2): {result.content[0].text}")

if __name__ == "__main__":
    asyncio.run(main())