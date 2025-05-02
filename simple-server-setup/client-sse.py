import asyncio
import nest_asyncio
from mcp import ClientSession
from mcp.client.sse import sse_client

nest_asyncio.apply()  # Needed to run interactive python

"""
Make sure:
1. The server is running before running this script.
2. The server is configured to use SSE transport.
3. The server is listening on port 8050.

To run the server:
uv run server.py
python3 server.py
"""

async def main():
    # Connect to the server using SSE transport
    async with sse_client("http://localhost:8050/sse") as (read_stream, write_stream):
        async with ClientSession(read_stream, write_stream) as session:
            # Initialize the session
            await session.initialize()

            # List the tools available
            tool_result = await session.list_tools()
            print("Available tools:")
            for tool in tool_result.tools:
                print(f" - {tool.name}: {tool.description}")

            # Call our calculator tool
            result = await session.call_tool("add", arguments={"a": 1, "b": 2})
            print(f"Result of add(1, 2): {result.content[0].text}")

if __name__ == "__main__":
    asyncio.run(main())