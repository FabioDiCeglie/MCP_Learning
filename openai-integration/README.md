# OpenAI Integration with MCP

This section demonstrates how to integrate the Model Context Protocol (MCP) with OpenAI's API to create a system where OpenAI can access and use tools provided by your MCP server.

## Overview

This example shows how to:

1. Create an MCP server that exposes a knowledge base tool
2. Connect OpenAI to this MCP server
3. Allow OpenAI to dynamically use the tools when responding to user queries

## Connection Methods

This example demonstrates using both **stdio transport** and **sse transport** for communication. The specific transport used can be configured within the `client.py` and `server.py` files by changing the `transport` variable.

- **stdio**: The client directly launches the server as a subprocess. No separate server process needs to be started manually.
- **sse**: The client connects to a running server via HTTP Server-Sent Events. The server must be started separately before the client.

If you want to split your client and server into separate applications (e.g., running the server on a different machine), you'll need to use the **SSE (Server-Sent Events) transport** instead.

### Data Flow Explanation

1. **User Query**: The user sends a query to the system (e.g., "What is our company's vacation policy?")
2. **OpenAI API**: OpenAI receives the query and available tools from the MCP server
3. **Tool Selection**: OpenAI decides which tools to use based on the query
4. **MCP Client**: The client receives OpenAI's tool call request and forwards it to the MCP server
5. **MCP Server**: The server executes the requested tool (e.g., retrieving knowledge base data)
6. **Response Flow**: The tool result flows back through the MCP client to OpenAI
7. **Final Response**: OpenAI generates a final response incorporating the tool data

## How OpenAI Executes Tools

OpenAI's function calling mechanism works with MCP tools through these steps:

1. **Tool Registration**: The MCP client converts MCP tools to OpenAI's function format
2. **Tool Choice**: OpenAI decides which tools to use based on the user query
3. **Tool Execution**: The MCP client executes the selected tools and returns results
4. **Context Integration**: OpenAI incorporates the tool results into its response

## The Role of MCP

MCP serves as a standardized bridge between AI models and your backend systems:

- **Standardization**: MCP provides a consistent interface for AI models to interact with tools
- **Abstraction**: MCP abstracts away the complexity of your backend systems
- **Security**: MCP allows you to control exactly what tools and data are exposed to AI models
- **Flexibility**: You can change your backend implementation without changing the AI integration
- **Reusability**: The big advantage is that you don't have to recreate the core logic for accessing the tool (like how to talk to the GitHub API, or how to query a specific database schema) for every different AI model or application you build. You build that logic once inside an MCP Server.

## Implementation Details

### Server (`server.py`)

The MCP server exposes a `get_knowledge_base` tool that retrieves Q&A pairs from a JSON file.

### Client (`client.py`)

The client:

1. Connects to the MCP server
2. Converts MCP tools to OpenAI's function format
3. Handles the communication between OpenAI and the MCP server
4. Processes tool results and generates final responses

### Knowledge Base (`data.json`)

Contains Q&A pairs about company policies that can be queried through the MCP server.

## Running the Example

1. Ensure you have the required dependencies installed.
2. Set up your OpenAI API key in the `.env` file.
3. **Choose Transport:** Decide whether to use `stdio` or `sse`. The default in the provided code is `sse`.
    - **SSE (Default):**
        1. Start the server: `python server.py`
        2. In a separate terminal, run the client: `python client.py`
    - **Stdio:**
        1. Modify the `transport` variable in both `client.py` and `server.py` to `"stdio"`.
        2. Run the client: `python client.py`. The client will automatically start the server process.

Note: The default configuration uses the **SSE transport**, which requires running the server separately first. If you switch the `transport` variable to `"stdio"` in both the client and server files, the client will manage the server process automatically.