import os
import json
from mcp.server.fastmcp import FastMCP

# Create an MCP server
mcp = FastMCP(
    name="Knowledge Base",
    host="0.0.0.0",  # only used for SSE transport (localhost)
    port=8050,  # only used for SSE transport (set this to any port)
)


@mcp.tool()
def search_knowledge_base() -> str:
    """Retrieve the entire knowledge base as a formatted string.

    Returns:
        A formatted string containing all Q&A pairs from the knowledge base.
    """
    try:
        data_path = os.path.join(os.path.dirname(__file__), "data.json")
        with open(data_path, "r") as f:
            data = json.load(f)
        
        data_text = "Here is the knowledge base:\n\n"

        if isinstance(data, list):
            for i, item in enumerate(data, 1):
                if isinstance(item, dict):
                    question = item.get('question', 'Unknown question')
                    answer = item.get('answer', 'Unknown answer')
                else:
                    question = f"Item {i}"
                    answer = str(item)

                data_text += f"Q{i}: {question}\n"
                data_text += f"A{i}: {answer}\n\n"
        else:
            data_text += f"Knowledge base content: {json.dumps(data, indent=2)}\n\n"

        return data_text
    except FileNotFoundError:
        return "Error: Knowledge base file not found"
    except json.JSONDecodeError:
        return "Error: Invalid JSON in knowledge base file"
    except Exception as e:
        return f"Error: {str(e)}"
    
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