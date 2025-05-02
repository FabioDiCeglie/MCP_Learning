# MCP Crash Course for Python Developers

The Model Context Protocol (MCP) is a powerful framework that enables developers to build AI applications with large language models (LLMs) by providing a standardized way to connect models with external data sources and tools. This crash course will guide you through the fundamentals of MCP, from understanding its core concepts to implementing servers and clients that leverage prompts, resources, and tools.

## Table of Contents

1. [Introduction and Context](./1-introduction-and-context/README.md)
2. [Understanding MCP](./2-understanding-mcp/README.md)
3. [Simple Server Setup with Python SDK](./3-simple-server-setup/README.md)
4. [OpenAI Integration](./4-openai-integration/README.md)
5. [MCP vs Function Calling](./5-mcp-vs-function-calling/README.md)
6. [Running with Docker](./6-run-with-docker/README.md)
7. [Lifecycle Management](./7-lifecycle-management/README.md)

## Setting Up Your Development Environment with uv

## Setup

1.  **Install `uv`:**
    If you haven't already, install `uv`:
    ```bash
    # Using curl (check uv documentation for other methods)
    curl -LsSf https://astral.sh/uv/install.sh | sh

    # Or using Homebrew on macOS/Linux
    brew install uv
    ```

2.  **Create a Virtual Environment:**
    Navigate to the project directory and create a virtual environment using `uv`:
    ```bash
    uv venv
    ```
    This will create a `.venv` directory.

3.  **Activate the Environment:**
    Activate the environment:
    *   **macOS/Linux:**
        ```bash
        source .venv/bin/activate
        ```
    *   **Windows (Command Prompt):**
        ```bash
        .venv\Scripts\activate.bat
        ```
    *   **Windows (PowerShell):**
        ```bash
        .venv\Scripts\Activate.ps1
        ```

4.  **Install Dependencies:**
    Install the required packages using `uv`:
    ```bash
    uv pip install -r requirements.txt
    ```
    *(Assuming your dependencies are listed in `requirements.txt`)*

The MCP CLI tools provide helpful utilities for development and testing:

```bash
# Test a server with the MCP Inspector
mcp dev server.py

# Install a server in Claude Desktop
mcp install server.py

# Run a server directly
mcp run server.py
```

## Resources and Next Steps

Key resources for deepening your MCP knowledge:

- [Model Context Protocol documentation](https://modelcontextprotocol.io)
- [Model Context Protocol specification](https://spec.modelcontextprotocol.io)
- [Python SDK GitHub repository](https://github.com/modelcontextprotocol/python-sdk)
- [Officially supported servers](https://github.com/modelcontextprotocol/servers)
- [MCP Core Architecture](https://modelcontextprotocol.io/docs/concepts/architecture)
