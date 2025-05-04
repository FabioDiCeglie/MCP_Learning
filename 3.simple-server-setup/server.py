from mcp.server.fastmcp import FastMCP
from dotenv import load_dotenv

load_dotenv('../.env')

# Create a new MCP server
mcp = FastMCP(
    api_key='Calculator',
    host='0.0.0.0', # Only used for SSE transport
    port=8050 # Only used for SSE transport ( set this to any port you want )
)

# Add a simple calculator tool
@mcp.tool()
def add(a: int, b: int) -> int:
    """Add two numbers together"""
    return a + b

# Run the server
if __name__ == "__main__":
    transport = "sse"
    if transport == "stdio":
        print("Running server in stdio mode")
        mcp.run(transport="stdio")
    elif transport == "sse":
        print("Running server in SSE mode")
        mcp.run(transport="sse")
    else:
        raise ValueError(f"Unknown transport: {transport}")