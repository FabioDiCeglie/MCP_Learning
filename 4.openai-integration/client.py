import asyncio
import json
from contextlib import AsyncExitStack
from typing import Any, Dict, List

import nest_asyncio
from dotenv import load_dotenv
from mcp import ClientSession, StdioServerParameters
from mcp.client.stdio import stdio_client
from openai import AsyncOpenAI
from mcp.client.sse import sse_client

load_dotenv(".env")

nest_asyncio.apply()

# Global variables to store session state
session = None
exit_stack = AsyncExitStack()
openai_client = AsyncOpenAI()
model = "gpt-4o"
stdio = None
write = None
transport = "sse"

async def connect_to_server(server_script_path: str = "server.py"):
    """Connect to an MCP server.

    Args:
        server_script_path (str): The path to the server script.
    """
    global session, stdio, write, exit_stack
    if transport == "stdio":
        # Server configuration
        server_params = StdioServerParameters(
            command= "python3",
            args=[server_script_path],
        )

        # Connect to the server using STDIO transport
        stdio_transport = await exit_stack.enter_async_context(stdio_client(server_params))
        stdio, write = stdio_transport
        session = await exit_stack.enter_async_context(ClientSession(stdio, write))

        # Initialize the connection
        await session.initialize()
    elif transport == "sse":
        """Make sure: The server is running before running this in SSE mode."""
        # Connect to the server using SSE transport
        read_stream, write_stream = await exit_stack.enter_async_context(
            sse_client("http://localhost:8050/sse")
        )
        session = await exit_stack.enter_async_context(
            ClientSession(read_stream, write_stream)
        )
        # Initialize the session
        await session.initialize()

    # List available tools
    tools_result = await session.list_tools()
    print("\nConnected to server with tools:")
    for tool in tools_result.tools:
        print(f"- {tool.name}: {tool.description}")

async def get_mcp_tools() -> List[Dict[str, Any]]:
    """Get available tools from the MCP server in OpenAI format.

    Returns:
        A list of tools in OpenAI format.
    """
    global session

    tools_result = await session.list_tools()
    return [
        {
            "type": "function",
            "function": {
                "name": tool.name,
                "description": tool.description,
                "parameters": tool.inputSchema,
            },
        }
        for tool in tools_result.tools
    ]

async def process_query(query: str) -> str:
    """Process a query using OpenAI and available MCP tools.
    
    Args:
        query (str): The user query.

    Returns:
        str: The response from the OpenAI API.
    """
    
    global session, openai_client, model

    # Get available tools
    tools = await get_mcp_tools()

    # Initial OpenAi API call
    response = await openai_client.chat.completions.create(
        model=model,
        messages=[
            {"role": "system", "content": query},
        ],
        tools=tools,
        tool_choice="auto",
    )

    # Get assistant's response
    assistant_message = response.choices[0].message

    # Initialize conversation with user query and assistant's response
    messages = [
        {"role": "user", "content": query},
        assistant_message,
    ]

    # Handle tool calls if present
    if assistant_message.tool_calls:
        # Process each tool calls in order
        for tool_call in assistant_message.tool_calls:
            # Execute the tool call
            result = await session.call_tool(
                tool_call.function.name,
                arguments=json.loads(tool_call.function.arguments),
            )

            messages.append({
                "role": "tool",
                "tool_call_id": tool_call.id,
                "content": result.content[0].text,
            })

            # Get final response from OpenAi with tools result
            final_response = await openai_client.chat.completions.create(
                model=model,
                messages=messages,
                tools=tools,
                tool_choice="none",
            )

            return final_response.choices[0].message.content
        
    # Return the final response
    return assistant_message.content
            
async def cleanup():
    """Clean up resources."""
    global exit_stack
    await exit_stack.aclose()

async def main():
    if transport == "stdio":
        print("Connecting to server in stdio mode")
        await connect_to_server("server.py")
    elif transport == "sse":
        print("Connecting to server in SSE mode")
        await connect_to_server("server.py")
    else:
        raise ValueError(f"Unknown transport: {transport}")

    # Example: Ask about company vacation policy
    query = "What is our company's vacation policy?"
    print(f"\nQuery: {query}")

    response = await process_query(query)
    print(f"\nResponse: {response}")

    await cleanup()

if __name__ == "__main__":
    asyncio.run(main())
    